from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.database import Base
from app.repositories.documents import DocumentRepository


def test_document_repository_persists_documents_and_chunks() -> None:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DocumentRepository(session)
        document = repository.add("Guide.md", "markdown", ["first chunk", "second chunk"])
        session.commit()
        document_id = document.id

    with Session(engine) as session:
        persisted = DocumentRepository(session).get(document_id)

        assert persisted is not None
        assert persisted.name == "Guide.md"
        assert [chunk.text for chunk in persisted.chunks] == ["first chunk", "second chunk"]


def test_document_repository_deletes_document_and_chunks() -> None:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        repository = DocumentRepository(session)
        document = repository.add("Guide.md", "markdown", ["content"])
        session.commit()
        repository.delete(document)
        session.commit()

        assert repository.get(document.id) is None
