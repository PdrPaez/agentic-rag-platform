from pathlib import Path

from fastapi.testclient import TestClient

from app.api.routes.documents import get_session
from app.db.database import Base, create_session_factory
from app.main import app


def test_document_api_upload_list_and_delete(tmp_path: Path) -> None:
    database_url = f"sqlite:///{tmp_path / 'test.db'}"
    session_factory = create_session_factory(database_url)
    Base.metadata.create_all(session_factory.kw["bind"])

    def override_session():
        with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    try:
        client = TestClient(app)
        upload = client.post("/api/documents", files={"file": ("notes.txt", b"Project notes")})

        assert upload.status_code == 201
        document_id = upload.json()["id"]
        assert client.get("/api/documents").json()[0]["name"] == "notes.txt"
        assert client.delete(f"/api/documents/{document_id}").status_code == 204
        assert client.get("/api/documents").json() == []
    finally:
        app.dependency_overrides.clear()
