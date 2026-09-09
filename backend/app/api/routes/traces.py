from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.observability.traces import get_trace

router = APIRouter(prefix="/traces")


class TraceResponse(BaseModel):
    request_id: str
    entries: list[dict[str, object]]


@router.get("/{request_id}", response_model=TraceResponse, summary="Inspect a request trace")
def trace(request_id: str) -> TraceResponse:
    entries = get_trace(request_id)
    if entries is None:
        raise HTTPException(status_code=404, detail="Trace not found")
    return TraceResponse(request_id=request_id, entries=entries)
