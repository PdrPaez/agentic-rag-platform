from collections.abc import Generator

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.observability.metrics import DOCUMENT_INGESTION_COUNT, ERROR_COUNT
from app.rag.runtime import get_embedder, vector_store
from app.repositories.documents import DocumentRepository
from app.services.document_ingestion import DocumentIngestionError, ingest_document

router = APIRouter(prefix="/documents")


class DocumentResponse(BaseModel):
    id: str
    name: str
    source_type: str
    chunk_count: int


def get_session() -> Generator[Session, None, None]:
    from app.db.runtime import session_factory

    with session_factory() as session:
        yield session


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a document",
)
async def upload_document(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> DocumentResponse:
    content = await file.read(get_settings().max_upload_size_bytes + 1)
    if len(content) > get_settings().max_upload_size_bytes:
        raise HTTPException(status_code=413, detail="The document exceeds the maximum upload size")
    try:
        settings = get_settings()
        extracted = ingest_document(
            file.filename or "document.txt",
            content,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
    except DocumentIngestionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    document = DocumentRepository(session).add(
        extracted.name, extracted.source_type, extracted.chunks
    )
    try:
        vectors = get_embedder().encode(extracted.chunks)
        vector_store.ensure_collection(get_embedder().dimension)
        vector_store.upsert(
            [chunk.id for chunk in document.chunks],
            vectors,
            [
                {
                    "document_id": document.id,
                    "document_name": document.name,
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.text,
                }
                for chunk in document.chunks
            ],
        )
        session.commit()
    except Exception as exc:
        session.rollback()
        ERROR_COUNT.labels("document_ingestion").inc()
        raise HTTPException(
            status_code=503, detail="Document embedding is temporarily unavailable"
        ) from exc
    DOCUMENT_INGESTION_COUNT.inc()
    return DocumentResponse(
        id=document.id,
        name=document.name,
        source_type=document.source_type,
        chunk_count=len(document.chunks),
    )


@router.get("", response_model=list[DocumentResponse], summary="List indexed documents")
def list_documents(session: Session = Depends(get_session)) -> list[DocumentResponse]:
    return [
        DocumentResponse(
            id=document.id,
            name=document.name,
            source_type=document.source_type,
            chunk_count=len(document.chunks),
        )
        for document in DocumentRepository(session).list()
    ]


@router.delete(
    "/{document_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an indexed document"
)
def delete_document(document_id: str, session: Session = Depends(get_session)) -> None:
    repository = DocumentRepository(session)
    document = repository.get(document_id)
    if document is not None:
        repository.delete(document)
        try:
            vector_store.delete_document(document_id)
            session.commit()
        except Exception as exc:
            session.rollback()
            ERROR_COUNT.labels("document_deletion").inc()
            raise HTTPException(
                status_code=503, detail="Document deletion is temporarily unavailable"
            ) from exc


def seed_demo_documents(session: Session = Depends(get_session)) -> list[DocumentResponse]:
    from pathlib import Path

    demo_directory = Path(__file__).resolve().parents[2] / "evaluation" / "documents"
    existing = {document.name for document in DocumentRepository(session).list()}
    seeded: list[DocumentResponse] = []
    settings = get_settings()
    for path in sorted(demo_directory.glob("*.md")):
        if path.name in existing:
            continue
        extracted = ingest_document(
            path.name,
            path.read_bytes(),
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )
        document = DocumentRepository(session).add(
            extracted.name, extracted.source_type, extracted.chunks
        )
        vectors = get_embedder().encode(extracted.chunks)
        vector_store.ensure_collection(get_embedder().dimension)
        vector_store.upsert(
            [chunk.id for chunk in document.chunks],
            vectors,
            [
                {
                    "document_id": document.id,
                    "document_name": document.name,
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.text,
                }
                for chunk in document.chunks
            ],
        )
        DOCUMENT_INGESTION_COUNT.inc()
        seeded.append(
            DocumentResponse(
                id=document.id,
                name=document.name,
                source_type=document.source_type,
                chunk_count=len(document.chunks),
            )
        )
    session.commit()
    return seeded
