from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db.models import ChunkRecord
from app.rag.embeddings import Embedder
from app.rag.hybrid import HybridCandidate, combine_results
from app.rag.lexical import LexicalIndex
from app.rag.vector_store import LocalVectorStore


class HybridRetriever:
    def __init__(
        self, embedder: Embedder, vector_store: LocalVectorStore, settings: Settings
    ) -> None:
        self.embedder = embedder
        self.vector_store = vector_store
        self.settings = settings

    def search(self, query: str, session: Session) -> list[HybridCandidate]:
        chunks = list(
            session.scalars(
                select(ChunkRecord).order_by(ChunkRecord.document_id, ChunkRecord.chunk_index)
            )
        )
        lexical_index = LexicalIndex()
        lexical_index.rebuild(chunks)
        lexical_matches = lexical_index.search(query, self.settings.retrieval_candidate_count)
        query_vector = self.embedder.encode([query])[0]
        vector_matches = self.vector_store.search(
            query_vector, self.settings.retrieval_candidate_count
        )
        return combine_results(
            lexical_matches,
            vector_matches,
            lexical_weight=self.settings.lexical_weight,
            vector_weight=self.settings.vector_weight,
            limit=self.settings.retrieval_candidate_count,
        )
