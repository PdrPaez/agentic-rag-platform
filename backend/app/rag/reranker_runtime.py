from functools import lru_cache

from app.core.config import get_settings
from app.rag.reranking import CrossEncoderReranker


@lru_cache
def get_reranker() -> CrossEncoderReranker:
    return CrossEncoderReranker(get_settings().reranker_model_name)
