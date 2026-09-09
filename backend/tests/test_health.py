import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app.core.config import Settings
from app.main import app


def test_health_endpoint_returns_service_status() -> None:
    response = TestClient(app).get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "agentic-rag-platform-api",
    }


def test_settings_parse_comma_separated_cors_origins() -> None:
    settings = Settings(cors_origins="http://localhost:5173, http://127.0.0.1:5173")

    assert settings.allowed_origins == [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


def test_public_openapi_routes_have_descriptions() -> None:
    paths = app.openapi()["paths"]

    assert "/api/demo/seed" in paths
    assert "/api/documents/demo/seed" not in paths
    assert paths["/api/chat"]["post"]["summary"] == "Ask the bounded RAG agent"
    assert paths["/api/demo/seed"]["post"]["summary"] == "Seed the demo corpus"


@pytest.mark.parametrize("field", ["max_context_characters", "retrieval_candidate_count", "final_context_count", "llm_timeout_seconds"])
def test_settings_reject_non_positive_runtime_limits(field: str) -> None:
    with pytest.raises(ValidationError):
        Settings(**{field: 0})
