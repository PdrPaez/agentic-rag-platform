from fastapi import APIRouter
from fastapi.responses import Response

from app.observability.metrics import metrics_payload

router = APIRouter()


@router.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(metrics_payload(), media_type="text/plain; version=0.0.4")
