from collections.abc import Sequence

from fastapi.testclient import TestClient

from app.api.routes import chat as chat_route
from app.api.routes.documents import get_session
from app.main import app
from app.rag.hybrid import HybridCandidate


class FakeRetriever:
    def search(self, question: str, session: object) -> list[HybridCandidate]:
        return [HybridCandidate("chunk-1", "doc-1", "Useful context", 1.0, 0.5, 0.8, "Guide.md")]


class EmptyRetriever:
    def search(self, question: str, session: object) -> list[HybridCandidate]:
        return []


class FakeReranker:
    def score(self, query: str, texts: Sequence[str]) -> list[float]:
        return [0.9 for _ in texts]


class FakeProvider:
    name = "mock"

    def generate(self, query: str, context: Sequence[str], tool_result: str | None = None) -> str:
        return f"Answer from {context[0]}"


class CalculatorProvider(FakeProvider):
    def generate(self, query: str, context: Sequence[str], tool_result: str | None = None) -> str:
        return f"Calculated {tool_result}"


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
