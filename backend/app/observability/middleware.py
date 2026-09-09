import logging
import re
from time import perf_counter
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.observability.metrics import ERROR_COUNT, REQUEST_COUNT, REQUEST_LATENCY

logger = logging.getLogger("agentic_rag_platform")
REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")


def _request_id(request: Request) -> str:
    supplied = request.headers.get("x-request-id", "")
    return supplied if REQUEST_ID_PATTERN.fullmatch(supplied) else str(uuid4())


class RequestObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = _request_id(request)
        request.state.request_id = request_id
        started = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            ERROR_COUNT.labels("unhandled_request").inc()
            raise
        duration = perf_counter() - started
        path = request.url.path
        REQUEST_COUNT.labels(request.method, path, str(response.status_code)).inc()
        REQUEST_LATENCY.labels(request.method, path).observe(duration)
        response.headers["x-request-id"] = request_id
        logger.info(
            "request_completed",
            extra={"request_id": request_id, "method": request.method, "path": path, "duration_ms": duration * 1000},
        )
        return response

