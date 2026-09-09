from pathlib import Path

from fastapi.testclient import TestClient

from app.api.routes import documents as documents_route
from app.api.routes.documents import get_session
from app.db.database import Base, create_session_factory
from app.main import app


def test_demo_seed_is_idempotent(tmp_path: Path) -> None:
    session_factory = create_session_factory(f"sqlite:///{tmp_path / 'demo.db'}")
    Base.metadata.create_all(session_factory.kw["bind"])

    def override_session():
        with session_factory() as session:
            yield session

    class FakeEmbedder:
        dimension = 2

        def encode(self, texts: list[str]) -> list[list[float]]:
            return [[1.0, 0.0] for _ in texts]

    class FakeVectorStore:
        def ensure_collection(self, dimension: int) -> None:
            pass

        def upsert(self, chunk_ids, vectors, payloads) -> None:
            pass

    original_embedder = documents_route.get_embedder
    original_store = documents_route.vector_store
    documents_route.get_embedder = lambda: FakeEmbedder()
    documents_route.vector_store = FakeVectorStore()
    app.dependency_overrides[get_session] = override_session
    try:
        client = TestClient(app)
        first = client.post("/api/demo/seed")
        second = client.post("/api/demo/seed")

        assert first.status_code == 200
        assert len(first.json()) == 5
        assert second.status_code == 200
        assert second.json() == []
    finally:
        documents_route.get_embedder = original_embedder
        documents_route.vector_store = original_store
        app.dependency_overrides.clear()
