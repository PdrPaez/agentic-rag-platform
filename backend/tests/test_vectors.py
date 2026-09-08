from pathlib import Path

from app.rag.vector_store import LocalVectorStore


def test_local_vector_store_upserts_searches_and_deletes_by_document(tmp_path: Path) -> None:
    store = LocalVectorStore(str(tmp_path / "vectors"), "chunks")
    store.ensure_collection(3)
    store.upsert(
        ["00000000-0000-0000-0000-000000000001", "00000000-0000-0000-0000-000000000002"],
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        [
            {"document_id": "doc-1", "text": "first"},
            {"document_id": "doc-2", "text": "second"},
        ],
    )

    matches = store.search([1.0, 0.0, 0.0], limit=2)

    assert matches[0].chunk_id == "00000000-0000-0000-0000-000000000001"
    assert matches[0].payload["document_id"] == "doc-1"
    store.delete_document("doc-1")
    assert [match.chunk_id for match in store.search([1.0, 0.0, 0.0], limit=2)] == [
        "00000000-0000-0000-0000-000000000002"
    ]
