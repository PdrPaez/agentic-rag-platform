from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routes.documents import DocumentResponse, get_session, seed_demo_documents

router = APIRouter()


@router.post("/demo/seed", response_model=list[DocumentResponse])
def seed_demo(session: Session = Depends(get_session)) -> list[DocumentResponse]:
    return seed_demo_documents(session)
