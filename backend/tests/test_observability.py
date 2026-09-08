from fastapi.testclient import TestClient

from app.main import app


def test_requests_return_request_id_and_metrics_endpoint_is_available() -> None:
    client = TestClient(app)
    response = client.get("/api/health", headers={"x-request-id": "request-test"})

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "request-test"
    metrics = client.get("/api/metrics")
    assert metrics.status_code == 200
    assert "rag_http_requests_total" in metrics.text
