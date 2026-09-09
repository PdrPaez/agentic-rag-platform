from app.evaluation.run import evaluate, load_cases, load_chunks


def test_bundled_evaluation_dataset_is_complete() -> None:
    assert len(load_cases()) == 29
    assert {chunk.document_id for chunk in load_chunks()} == {
        "architecture.md", "refund-policy.md", "incident-response.md", "engineering-handbook.md", "support-procedures.md"
    }


def test_evaluation_executes_all_retrieval_stages() -> None:
    stages, coverage, latency = evaluate()

    assert [stage.name for stage in stages] == ["BM25", "Vector", "Hybrid", "Hybrid + reranking"]
    assert all(0 <= stage.hit_rate_at_5 <= 1 for stage in stages)
    assert all(0 <= stage.mean_reciprocal_rank <= 1 for stage in stages)
    assert 0 <= coverage <= 1
    assert latency >= 0
