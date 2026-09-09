from collections.abc import Sequence

from fastapi.testclient import TestClient

from app.api.routes import chat as chat_route
from app.api.routes.documents import get_session
from app.main import app
from app.observability.traces import get_trace
from app.rag.hybrid import HybridCandidate


class FakeRetriever:
    def search(self, question: str, session: object) -> list[HybridCandidate]:
        return [HybridCandidate("chunk-1", "doc-1", "Useful context", 1.0, 0.5, 0.8, "Guide.md")]


class EmptyRetriever:
    def search(self, question: str, session: object) -> list[HybridCandidate]:
        return []


class OversizedRetriever:
    def search(self, question: str, session: object) -> list[HybridCandidate]:
        return [HybridCandidate("large-chunk", "doc-1", "x" * 6001, 1.0, 0.5, 0.8, "Guide.md")]


class FakeReranker:
    def score(self, query: str, texts: Sequence[str]) -> list[float]:
        return [0.9 for _ in texts]


class FakeProvider:
    name = "mock"

    def generate(self, query: str, context: Sequence[str], tool_result: str | None = None) -> str:
        if not context:
            return "I could not find relevant information in the knowledge base."
        return f"Answer from {context[0]}"


class CalculatorProvider(FakeProvider):
    def generate(self, query: str, context: Sequence[str], tool_result: str | None = None) -> str:
        return f"Calculated {tool_result}"


class UnavailableProvider(FakeProvider):
    def generate(self, query: str, context: Sequence[str], tool_result: str | None = None) -> str:
        raise RuntimeError("The LLM provider is unavailable")


def test_chat_returns_structured_answer_and_citation() -> None:
    app.dependency_overrides[get_session] = lambda: iter([object()])
    original = (chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider)
    chat_route.get_retriever = lambda: FakeRetriever()
    chat_route.get_reranker = lambda: FakeReranker()
    chat_route.get_provider = lambda: FakeProvider()
    try:
        response = TestClient(app).post("/api/chat", json={"question": "What is useful?"})

        body = response.json()
        assert response.status_code == 200
        assert body["answer"] == "Answer from Useful context"
        assert body["answer_status"] == "answered"
        assert body["citations"][0]["document_name"] == "Guide.md"
        assert body["diagnostics"]["retrieved_chunks"] == 1
    finally:
        chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider = original
        app.dependency_overrides.clear()


def test_chat_uses_calculator_tool_without_citations() -> None:
    app.dependency_overrides[get_session] = lambda: iter([object()])
    original = (chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider)
    chat_route.get_retriever = lambda: FakeRetriever()
    chat_route.get_reranker = lambda: FakeReranker()
    chat_route.get_provider = lambda: CalculatorProvider()
    try:
        response = TestClient(app).post("/api/chat", json={"question": "Calculate 20 / 4"})

        body = response.json()
        assert response.status_code == 200
        assert body["answer"] == "Calculated 5"
        assert body["citations"] == []
        assert body["tools_used"] == ["calculator"]
        assert body["answer_status"] == "tool_result"
    finally:
        chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider = original
        app.dependency_overrides.clear()


def test_chat_reports_insufficient_context_without_citations() -> None:
    app.dependency_overrides[get_session] = lambda: iter([object()])
    original = (chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider)
    chat_route.get_retriever = lambda: EmptyRetriever()
    chat_route.get_reranker = lambda: FakeReranker()
    chat_route.get_provider = lambda: FakeProvider()
    try:
        response = TestClient(app).post("/api/chat", json={"question": "Unknown topic?"})

        body = response.json()
        assert response.status_code == 200
        assert body["answer_status"] == "insufficient_context"
        assert body["citations"] == []
        assert body["tools_used"] == []
    finally:
        chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider = original
        app.dependency_overrides.clear()


def test_chat_returns_service_unavailable_when_provider_is_down() -> None:
    app.dependency_overrides[get_session] = lambda: iter([object()])
    original = (chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider)
    chat_route.get_retriever = lambda: FakeRetriever()
    chat_route.get_reranker = lambda: FakeReranker()
    chat_route.get_provider = lambda: UnavailableProvider()
    try:
        response = TestClient(app).post("/api/chat", json={"question": "What is useful?"})

        assert response.status_code == 503
        assert response.json()["detail"] == "The LLM provider is unavailable"
        request_id = response.headers["x-request-id"]
        assert any(stage["stage"] == "generation_failed" for stage in (get_trace(request_id) or []))
    finally:
        chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider = original
        app.dependency_overrides.clear()


def test_chat_returns_bad_request_for_invalid_calculation() -> None:
    app.dependency_overrides[get_session] = lambda: iter([object()])
    original = (chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider)
    chat_route.get_retriever = lambda: FakeRetriever()
    chat_route.get_reranker = lambda: FakeReranker()
    chat_route.get_provider = lambda: FakeProvider()
    try:
        response = TestClient(app).post("/api/chat", json={"question": "Calculate 1 / 0"})

        assert response.status_code == 400
        assert response.json()["detail"] == "The requested tool operation is invalid"
    finally:
        chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider = original
        app.dependency_overrides.clear()


def test_chat_reports_partial_when_context_budget_truncates() -> None:
    app.dependency_overrides[get_session] = lambda: iter([object()])
    original = (chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider)
    chat_route.get_retriever = lambda: OversizedRetriever()
    chat_route.get_reranker = lambda: FakeReranker()
    chat_route.get_provider = lambda: FakeProvider()
    try:
        response = TestClient(app).post("/api/chat", json={"question": "Summarize the guide"})

        body = response.json()
        assert response.status_code == 200
        assert body["answer_status"] == "partial"
        assert body["citations"][0]["chunk_id"] == "large-chunk"
    finally:
        chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider = original
        app.dependency_overrides.clear()
