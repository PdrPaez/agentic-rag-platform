"""Deterministic answer-behavior checks for the bundled evaluation corpus."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from app.evaluation.run import EvaluationCase, _canonical_tokens
from app.rag.hybrid import HybridCandidate


@dataclass(frozen=True)
class AnswerBehaviorSummary:
    cases: int
    answerable_cases: int
    abstention_cases: int
    abstention_accuracy: float
    citation_presence_accuracy: float
    expected_fact_coverage: float


def evaluate_answer_behavior(
    cases: Sequence[EvaluationCase],
    retrieved: Sequence[Sequence[HybridCandidate]],
) -> AnswerBehaviorSummary:
    if len(cases) != len(retrieved):
        raise ValueError("Cases and retrieved results must have the same length")
    if not cases:
        raise ValueError("Answer behavior evaluation requires at least one case")

    abstention_correct = 0
    citation_correct = 0
    fact_coverages: list[float] = []
    answerable_cases = 0
    for case, candidates in zip(cases, retrieved, strict=True):
        should_abstain = not case.expected_document and not case.expected_facts
        has_evidence = bool(candidates)
        abstention_correct += int((not has_evidence) == should_abstain)
        citation_correct += int(has_evidence == (not should_abstain))
        if not should_abstain:
            answerable_cases += 1
        corpus = " ".join(_canonical_tokens(" ".join(candidate.text for candidate in candidates)))
        fact_coverages.append(
            sum(" ".join(_canonical_tokens(fact)) in corpus for fact in case.expected_facts)
            / len(case.expected_facts)
            if case.expected_facts
            else 1.0
        )

    return AnswerBehaviorSummary(
        cases=len(cases),
        answerable_cases=answerable_cases,
        abstention_cases=len(cases) - answerable_cases,
        abstention_accuracy=abstention_correct / len(cases),
        citation_presence_accuracy=citation_correct / len(cases),
        expected_fact_coverage=sum(fact_coverages) / len(fact_coverages),
    )
