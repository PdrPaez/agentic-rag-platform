from app.db.models import ChunkRecord
from app.rag.lexical import LexicalIndex, tokenize


def test_tokenize_is_case_insensitive_and_ignores_punctuation() -> None:
    assert tokenize("Hybrid Retrieval, v2!") == ["hybrid", "retrieval", "v2"]


def test_lexical_index_ranks_matching_chunk_and_rebuilds() -> None:
    index = LexicalIndex()
    index.rebuild(
        [
            ChunkRecord(id="chunk-a", document_id="doc-a", chunk_index=0, text="Python deployment guide"),
            ChunkRecord(id="chunk-b", document_id="doc-b", chunk_index=0, text="Vector search guide"),
            ChunkRecord(id="chunk-c", document_id="doc-c", chunk_index=0, text="Frontend interface guide"),
        ]
    )

    matches = index.search("python deployment")

    assert matches[0].chunk_id == "chunk-a"
    assert matches[0].document_id == "doc-a"
    index.rebuild([])
    assert index.search("python") == []
