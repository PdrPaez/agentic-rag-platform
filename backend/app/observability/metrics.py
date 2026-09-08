from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter("rag_http_requests_total", "Total HTTP requests", ["method", "path", "status"])
REQUEST_LATENCY = Histogram("rag_http_request_latency_seconds", "HTTP request latency", ["method", "path"])


def metrics_payload() -> bytes:
    return generate_latest()

