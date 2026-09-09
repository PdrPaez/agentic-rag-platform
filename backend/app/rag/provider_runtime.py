from functools import lru_cache

from app.core.config import get_settings
from app.llm.providers import LLMProvider, create_provider


@lru_cache
def get_provider() -> LLMProvider:
    settings = get_settings()
    return create_provider(
        settings.llm_provider,
        settings.llm_model_name,
        settings.llm_api_key,
        settings.llm_base_url,
        settings.llm_timeout_seconds,
    )

