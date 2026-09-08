from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import ChunkRecord, DocumentRecord


class DocumentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str, source_type: str, chunks: list[str]) -> DocumentRecord:
        document = DocumentRecord(name=name, source_type=source_type)
        document.chunks = [ChunkRecord(chunk_index=index, text=text) for index, text in enumerate(chunks)]
        self.session.add(document)
        self.session.flush()
        return document

    def list(self) -> list[DocumentRecord]:
        statement = select(DocumentRecord).options(selectinload(DocumentRecord.chunks)).order_by(DocumentRecord.name)
        return list(self.session.scalars(statement))

    def get(self, document_id: str) -> DocumentRecord | None:
        statement = select(DocumentRecord).where(DocumentRecord.id == document_id).options(selectinload(DocumentRecord.chunks))
        return self.session.scalar(statement)

    def delete(self, document: DocumentRecord) -> None:
        self.session.delete(document)

