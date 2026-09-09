from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic RAG Platform API"
    app_version: str = "0.1.0"
    environment: str = "development"
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    database_url: str = "sqlite:///./data/agentic_rag.db"
    max_upload_size_bytes: int = Field(default=10 * 1024 * 1024, gt=0)
    vector_storage_path: str = "./qdrant_storage"
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    vector_collection_name: str = "document_chunks"
    reranker_model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    llm_provider: str = "mock"
    llm_model_name: str = "gpt-4o-mini"
    llm_api_key: str | None = None
    llm_base_url: str = "https://api.openai.com/v1"
    retrieval_candidate_count: int = Field(default=12, gt=0)
    final_context_count: int = Field(default=5, gt=0)
    lexical_weight: float = 0.4
    vector_weight: float = 0.6
    chunk_size: int = 800
    chunk_overlap: int = 150
    max_context_characters: int = Field(default=6000, gt=0)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

