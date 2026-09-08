from fastapi.testclient import TestClient

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
