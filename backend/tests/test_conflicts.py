from app.agents.orchestrator import detect_conflicting_evidence
from app.rag.hybrid import HybridCandidate


def _candidate(chunk_id: str, text: str) -> HybridCandidate:
    return HybridCandidate(chunk_id, f"{chunk_id}.md", text, 1.0, 1.0, 1.0)


def test_detects_divergent_numeric_evidence_for_shared_terms() -> None:
    candidates = [
        _candidate("policy-a", "The refund window is 30 calendar days."),
        _candidate("policy-b", "The refund window is 45 calendar days."),
    ]

    assert detect_conflicting_evidence("What is the refund window?", candidates) is True


def test_ignores_unrelated_numeric_evidence() -> None:
    candidates = [
        _candidate("policy-a", "The refund window is 30 calendar days."),
        _candidate("status-b", "The incident response target is 15 minutes."),
    ]

    assert detect_conflicting_evidence("What is the refund window?", candidates) is False
