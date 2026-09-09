from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str


@router.get("/health", response_model=HealthResponse, summary="Check service health")
def health() -> HealthResponse:
    return HealthResponse(status="ok", service="agentic-rag-platform-api")
