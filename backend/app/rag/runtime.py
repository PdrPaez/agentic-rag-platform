from functools import lru_cache

from app.core.config import get_settings
from app.rag.embeddings import SentenceTransformerEmbedder
from app.rag.vector_store import LocalVectorStore

settings = get_settings()
vector_store = LocalVectorStore(settings.vector_storage_path, settings.vector_collection_name)


@lru_cache
def get_embedder() -> SentenceTransformerEmbedder:
    return SentenceTransformerEmbedder(settings.embedding_model_name)
