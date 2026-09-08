from collections.abc import Sequence

from fastapi.testclient import TestClient

from app.api.routes import chat as chat_route
from app.api.routes.documents import get_session
from app.main import app
from app.rag.hybrid import HybridCandidate


class FakeRetriever:
    def search(self, question: str, session: object) -> list[HybridCandidate]:
        return [HybridCandidate("chunk-1", "doc-1", "Useful context", 1.0, 0.5, 0.8, "Guide.md")]


class FakeReranker:
    def score(self, query: str, texts: Sequence[str]) -> list[float]:
        return [0.9 for _ in texts]


class FakeProvider:
    name = "mock"

    def generate(self, query: str, context: Sequence[str], tool_result: str | None = None) -> str:
        return f"Answer from {context[0]}"


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
        assert body["citations"][0]["document_name"] == "Guide.md"
        assert body["diagnostics"]["retrieved_chunks"] == 1
    finally:
        chat_route.get_retriever, chat_route.get_reranker, chat_route.get_provider = original
        app.dependency_overrides.clear()
