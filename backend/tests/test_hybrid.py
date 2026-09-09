import pytest

from app.rag.hybrid import combine_results
from app.rag.lexical import LexicalMatch
from app.rag.normalization import min_max_normalize
from app.rag.vector_store import VectorMatch


def test_min_max_normalize_handles_empty_and_identical_scores() -> None:
    assert min_max_normalize([]) == []
    assert min_max_normalize([0.0, 0.0]) == [0.0, 0.0]
    assert min_max_normalize([3.0, 3.0]) == [1.0, 1.0]
    assert min_max_normalize([1.0, 2.0, 3.0]) == [0.0, 0.5, 1.0]


def test_combine_results_merges_by_chunk_and_retains_diagnostics() -> None:
    lexical = [LexicalMatch("chunk-a", 2.0, "alpha", "doc-a")]
    vectors = [
        VectorMatch("chunk-a", 0.6, {"document_id": "doc-a", "text": "alpha"}),
        VectorMatch("chunk-b", 0.9, {"document_id": "doc-b", "text": "beta"}),
    ]

    results = combine_results(lexical, vectors, lexical_weight=0.3, vector_weight=0.7)

    assert results[0].chunk_id == "chunk-b"
    assert results[0].vector_score == 1.0
    assert results[1].bm25_score == 1.0


def test_combine_results_rejects_invalid_weights() -> None:
    with pytest.raises(ValueError):
        combine_results([], [], lexical_weight=0.0, vector_weight=0.0)


def test_combine_results_breaks_score_ties_by_chunk_id() -> None:
    results = combine_results(
        [LexicalMatch("b", 1.0, "B", "doc"), LexicalMatch("a", 1.0, "A", "doc")],
        [],
    )

    assert [candidate.chunk_id for candidate in results] == ["a", "b"]
