from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.routes.documents import DocumentResponse, get_session, seed_demo_documents
from app.observability.metrics import ERROR_COUNT

router = APIRouter()


@router.post("/demo/seed", response_model=list[DocumentResponse], summary="Seed the demo corpus")
def seed_demo(session: Session = Depends(get_session)) -> list[DocumentResponse]:
    try:
        return seed_demo_documents(session)
    except Exception as exc:
        session.rollback()
        ERROR_COUNT.labels("document_ingestion").inc()
        raise HTTPException(
            status_code=503, detail="The demo corpus is temporarily unavailable"
        ) from exc
