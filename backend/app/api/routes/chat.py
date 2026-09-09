from time import perf_counter
from typing import Literal
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.agents.orchestrator import BoundedOrchestrator
from app.api.routes.documents import get_session
from app.core.config import get_settings
from app.observability.metrics import (
    ANSWER_STATUS_COUNT,
    FINAL_CONTEXT_CHUNKS,
    GENERATION_LATENCY,
    PROVIDER_FAILURE_COUNT,
    PROVIDER_REQUEST_COUNT,
    RETRIEVAL_LATENCY,
)
from app.observability.traces import record_trace
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
    context_truncated: bool
    context_chunks: int
    conflict_detected: bool
    retrieval: list[RetrievalDiagnostic]


class ChatResponse(BaseModel):
    answer: str
    answer_status: Literal["answered", "partial", "insufficient_context", "tool_result"]
    citations: list[Citation]
    tools_used: list[str]
    diagnostics: ChatDiagnostics


def get_retriever() -> HybridRetriever:
    return HybridRetriever(get_embedder(), vector_store, get_settings())


class TimedProvider:
    def __init__(self, provider: object, timings: dict[str, float], request_id: str) -> None:
        self.provider = provider
        self.timings = timings
        self.request_id = request_id
        self.name = provider.name

    def generate(self, question: str, context: list[str], tool_result: str | None = None) -> str:
        if tool_result is not None:
            record_trace(self.request_id, "tool_called", 0.0, tools=["calculator"])
        record_trace(self.request_id, "generation_started", 0.0, provider=self.name)
        started = perf_counter()
        PROVIDER_REQUEST_COUNT.labels(self.name).inc()
        try:
            answer = self.provider.generate(question, context, tool_result)
        except RuntimeError:
            PROVIDER_FAILURE_COUNT.labels(self.name).inc()
            record_trace(self.request_id, "generation_failed", 0.0, provider=self.name)
            raise
        self.timings["generation_latency_ms"] = (perf_counter() - started) * 1000
        record_trace(self.request_id, "generation_completed", self.timings["generation_latency_ms"], provider=self.name)
        return answer


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Ask the bounded RAG agent",
    description="Retrieve grounded context, optionally use the calculator, and return citations plus execution diagnostics.",
)
def chat(payload: ChatRequest, request: Request, session: Session = Depends(get_session)) -> ChatResponse:
    request_id = getattr(request.state, "request_id", request.headers.get("x-request-id", str(uuid4())))
    started = perf_counter()
    record_trace(request_id, "request_received", 0.0, operation="chat")
    timings: dict[str, float] = {"retrieval_latency_ms": 0.0, "generation_latency_ms": 0.0}

    def retrieve(question: str):
        record_trace(request_id, "retrieval_started", 0.0, query_length=len(question))
        retrieval_started = perf_counter()
        candidates = get_retriever().search(question, session)
        timings["retrieval_latency_ms"] = (perf_counter() - retrieval_started) * 1000
        RETRIEVAL_LATENCY.observe(timings["retrieval_latency_ms"] / 1000)
        record_trace(request_id, "retrieval_completed", timings["retrieval_latency_ms"], candidates=len(candidates))
        if candidates:
            record_trace(request_id, "tool_called", 0.0, tools=["search_knowledge_base"])
        return candidates

    def rank(question: str, candidates):
        rank_started = perf_counter()
        ranked = rerank_candidates(question, candidates, get_reranker(), get_settings().final_context_count)
        record_trace(request_id, "reranking_completed", (perf_counter() - rank_started) * 1000, candidates=len(ranked))
        return ranked

    try:
        result = BoundedOrchestrator(
            TimedProvider(get_provider(), timings, request_id),
            retrieve,
            rank,
            max_context_characters=get_settings().max_context_characters,
        ).run(payload.question)
    except RuntimeError as exc:
        if str(exc) != "The LLM provider is unavailable":
            raise
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="The requested tool operation is invalid") from exc
    GENERATION_LATENCY.observe(timings["generation_latency_ms"] / 1000)
    reranked = result.ranked_candidates
    answer = result.answer
    if result.conflict_detected:
        answer = f"{answer}\n\nThe corpus contains conflicting evidence. Review the cited sources before relying on this answer."
    generation_latency_ms = timings["generation_latency_ms"]
    diagnostics = ChatDiagnostics(
        request_id=request_id,
        retrieved_chunks=len(result.candidates),
        reranked_chunks=len(reranked),
        total_latency_ms=(perf_counter() - started) * 1000,
        retrieval_latency_ms=timings["retrieval_latency_ms"],
        generation_latency_ms=generation_latency_ms,
        provider=get_provider().name,
        estimated_input_tokens=len(payload.question.split()) + sum(len(candidate.text.split()) for candidate, _ in reranked),
            estimated_output_tokens=len(answer.split()),
            context_truncated=result.context_truncated,
            context_chunks=result.context_chunks,
            conflict_detected=result.conflict_detected,
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
    answer_status = (
        "tool_result" if "calculator" in result.tools_used
        else "partial" if result.context_truncated or result.conflict_detected
        else "answered" if reranked
        else "insufficient_context"
    )
    ANSWER_STATUS_COUNT.labels(answer_status).inc()
    FINAL_CONTEXT_CHUNKS.set(result.context_chunks)
    return ChatResponse(
        answer=answer,
        answer_status=answer_status,
        citations=[
            Citation(
                document_id=candidate.document_id,
                document_name=candidate.document_name or candidate.document_id,
                chunk_id=candidate.chunk_id,
                excerpt=candidate.text[:240],
            )
            for candidate, _ in reranked
        ],
        tools_used=result.tools_used,
        diagnostics=diagnostics,
    )
