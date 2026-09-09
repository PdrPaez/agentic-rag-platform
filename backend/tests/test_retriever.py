from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db.database import Base
from app.db.models import ChunkRecord, DocumentRecord
from app.rag.retriever import HybridRetriever


class FakeEmbedder:
    def encode(self, texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0, 0.0] for _ in texts]


class FakeVectorStore:
    def search(self, vector: list[float], limit: int) -> list:
        return []


def test_retriever_rebuilds_lexical_index_from_persisted_chunks(tmp_path: Path) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'retrieval.db'}")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        document = DocumentRecord(id="doc-1", name="Guide.md", source_type="md")
        document.chunks = [ChunkRecord(id="chunk-1", chunk_index=0, text="Python deployment guide")]
        session.add(document)
        session.commit()

        results = HybridRetriever(FakeEmbedder(), FakeVectorStore(), Settings()).search(
            "python", session
        )

    assert results[0].chunk_id == "chunk-1"
    assert results[0].bm25_score == 1.0
