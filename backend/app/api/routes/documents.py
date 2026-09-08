from collections.abc import Generator

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.config import get_settings
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


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
) -> DocumentResponse:
    content = await file.read(get_settings().max_upload_size_bytes + 1)
    if len(content) > get_settings().max_upload_size_bytes:
        raise HTTPException(status_code=413, detail="The document exceeds the maximum upload size")
    try:
        extracted = ingest_document(file.filename or "document.txt", content)
    except DocumentIngestionError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    document = DocumentRepository(session).add(extracted.name, extracted.source_type, extracted.chunks)
    session.commit()
    return DocumentResponse(
        id=document.id,
        name=document.name,
        source_type=document.source_type,
        chunk_count=len(document.chunks),
    )


@router.get("", response_model=list[DocumentResponse])
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


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str, session: Session = Depends(get_session)) -> None:
    repository = DocumentRepository(session)
    document = repository.get(document_id)
    if document is not None:
        repository.delete(document)
        session.commit()

