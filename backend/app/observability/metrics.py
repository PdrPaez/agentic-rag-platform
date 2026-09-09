from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter("rag_http_requests_total", "Total HTTP requests", ["method", "path", "status"])
REQUEST_LATENCY = Histogram("rag_http_request_latency_seconds", "HTTP request latency", ["method", "path"])
RETRIEVAL_LATENCY = Histogram("rag_retrieval_latency_seconds", "Retrieval stage latency")
GENERATION_LATENCY = Histogram("rag_generation_latency_seconds", "Generation stage latency")
DOCUMENT_INGESTION_COUNT = Counter("rag_document_ingestion_total", "Documents ingested")
ERROR_COUNT = Counter("rag_errors_total", "Application errors", ["category"])
PROVIDER_REQUEST_COUNT = Counter("rag_provider_requests_total", "LLM provider requests", ["provider"])
PROVIDER_FAILURE_COUNT = Counter("rag_provider_failures_total", "LLM provider failures", ["provider"])
ANSWER_STATUS_COUNT = Counter("rag_answer_status_total", "Responses by grounding status", ["status"])


def metrics_payload() -> bytes:
    return generate_latest()

