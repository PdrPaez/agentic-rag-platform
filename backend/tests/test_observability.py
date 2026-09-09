from fastapi.testclient import TestClient

from app.main import app
from app.observability.traces import record_trace


def test_requests_return_request_id_and_metrics_endpoint_is_available() -> None:
    client = TestClient(app)
    response = client.get("/api/health", headers={"x-request-id": "request-test"})

    assert response.status_code == 200
    assert response.headers["x-request-id"] == "request-test"
    metrics = client.get("/api/metrics")
    assert metrics.status_code == 200
    assert "rag_http_requests_total" in metrics.text
    assert "rag_retrieval_latency_seconds" in metrics.text
    assert "rag_document_ingestion_total" in metrics.text
    assert client.get("/health").status_code == 200
    assert client.get("/metrics").status_code == 200


def test_trace_endpoint_returns_recorded_trace() -> None:
    record_trace("trace-test", "request_received", 0.0, operation="test")

    response = TestClient(app).get("/api/traces/trace-test")

    assert response.status_code == 200
    assert response.json()["entries"][0]["stage"] == "request_received"
    assert TestClient(app).get("/api/traces/missing").status_code == 404
