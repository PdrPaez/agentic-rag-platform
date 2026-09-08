from time import perf_counter
from uuid import uuid4

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.routes.documents import get_session
from app.core.config import get_settings
from app.rag.provider_runtime import get_provider
from app.rag.reranker_runtime import get_reranker
from app.rag.reranking import rerank_candidates
from app.rag.retriever import HybridRetriever
from app.rag.runtime import get_embedder, vector_store

router = APIRouter()


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class Citation(BaseModel):
    document_id: str
    document_name: str
    chunk_id: str
    excerpt: str


class RetrievalDiagnostic(BaseModel):
    chunk_id: str
    document_name: str
    bm25_score: float
    vector_score: float
    hybrid_score: float
    reranker_score: float


class ChatDiagnostics(BaseModel):
    request_id: str
    retrieved_chunks: int
    reranked_chunks: int
    total_latency_ms: float
    retrieval_latency_ms: float
    generation_latency_ms: float
    provider: str
    estimated_input_tokens: int
    estimated_output_tokens: int
    retrieval: list[RetrievalDiagnostic]


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
    tools_used: list[str]
    diagnostics: ChatDiagnostics


def get_retriever() -> HybridRetriever:
    return HybridRetriever(get_embedder(), vector_store, get_settings())


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, session: Session = Depends(get_session)) -> ChatResponse:
    request_id = str(uuid4())
    started = perf_counter()
    retrieval_started = perf_counter()
    candidates = get_retriever().search(request.question, session)
    retrieval_latency_ms = (perf_counter() - retrieval_started) * 1000
    reranked = rerank_candidates(
        request.question, candidates, get_reranker(), get_settings().final_context_count
    )
    generation_started = perf_counter()
    answer = get_provider().generate(request.question, [candidate.text for candidate, _ in reranked])
    generation_latency_ms = (perf_counter() - generation_started) * 1000
    diagnostics = ChatDiagnostics(
        request_id=request_id,
        retrieved_chunks=len(candidates),
        reranked_chunks=len(reranked),
        total_latency_ms=(perf_counter() - started) * 1000,
        retrieval_latency_ms=retrieval_latency_ms,
        generation_latency_ms=generation_latency_ms,
        provider=get_provider().name,
        estimated_input_tokens=len(request.question.split()) + sum(len(candidate.text.split()) for candidate, _ in reranked),
        estimated_output_tokens=len(answer.split()),
        retrieval=[
            RetrievalDiagnostic(
                chunk_id=candidate.chunk_id,
                document_name=candidate.document_name or candidate.document_id,
                bm25_score=candidate.bm25_score,
                vector_score=candidate.vector_score,
                hybrid_score=candidate.hybrid_score,
                reranker_score=score,
            )
            for candidate, score in reranked
        ],
    )
    return ChatResponse(
        answer=answer,
        citations=[
            Citation(
                document_id=candidate.document_id,
                document_name=candidate.document_name or candidate.document_id,
                chunk_id=candidate.chunk_id,
                excerpt=candidate.text[:240],
            )
            for candidate, _ in reranked
        ],
        tools_used=[],
        diagnostics=diagnostics,
    )
