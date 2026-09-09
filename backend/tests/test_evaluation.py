import pytest

from app.evaluation.answer_behavior import evaluate_answer_behavior
from app.evaluation.run import EvaluationCase, evaluate, load_cases, load_chunks
from app.rag.hybrid import HybridCandidate


def test_bundled_evaluation_dataset_is_complete() -> None:
    cases = load_cases()
    assert len(cases) == 30
    assert {chunk.document_id for chunk in load_chunks()} == {
        "architecture.md", "refund-policy.md", "incident-response.md", "engineering-handbook.md", "support-procedures.md"
    }
    negative_cases = [case for case in cases if not case.expected_document and not case.expected_facts]
    assert 0.20 <= len(negative_cases) / len(cases) <= 0.30


def test_evaluation_executes_all_retrieval_stages() -> None:
    stages, coverage, latency = evaluate()

    assert [stage.name for stage in stages] == ["BM25", "Vector", "Hybrid", "Hybrid + reranking"]
    assert all(0 <= stage.hit_rate_at_5 <= 1 for stage in stages)
    assert all(0 <= stage.mean_reciprocal_rank <= 1 for stage in stages)
    assert 0 <= coverage <= 1
    assert latency >= 0


def test_answer_behavior_checks_abstention_citations_and_fact_coverage() -> None:
    cases = [
        EvaluationCase("known", "guide.md", ("Qdrant",)),
        EvaluationCase("unknown", None, ()),
    ]
    candidate = HybridCandidate("chunk-1", "guide.md", "Qdrant stores vectors", 1.0, 1.0, 1.0)

    summary = evaluate_answer_behavior(cases, [[candidate], []])

    assert summary.abstention_accuracy == 1
    assert summary.citation_presence_accuracy == 1
    assert summary.expected_fact_coverage == 1


def test_answer_behavior_rejects_mismatched_inputs() -> None:
    with pytest.raises(ValueError, match="same length"):
        evaluate_answer_behavior([EvaluationCase("known", "guide.md", ("fact",))], [])
