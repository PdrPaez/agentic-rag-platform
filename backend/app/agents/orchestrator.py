import re
from collections.abc import Callable
from dataclasses import dataclass

from app.agents.tools.calculator import calculate
from app.agents.tools.search import search_knowledge_base
from app.llm.providers import LLMProvider
from app.rag.hybrid import HybridCandidate

MAX_STEPS = 3
MAX_CONTEXT_CHARACTERS = 6000
CALCULATION_PATTERN = re.compile(
    r"(?:calculate|compute|what is)\s+([0-9+\-*/().% ]+?)[?!.]*$", re.IGNORECASE
)


@dataclass(frozen=True)
class OrchestrationResult:
    answer: str
    candidates: list[HybridCandidate]
    ranked_candidates: list[tuple[HybridCandidate, float]]
    tools_used: list[str]
    steps: int
    context_truncated: bool = False
    context_chunks: int = 0
    conflict_detected: bool = False


def detect_conflicting_evidence(question: str, candidates: list[HybridCandidate]) -> bool:
    """Detect divergent numeric evidence shared by multiple relevant sources."""
    question_terms = set(re.findall(r"[a-zA-Z]{4,}", question.lower()))
    evidence: list[tuple[str, set[str], set[str]]] = []
    for candidate in candidates:
        terms = set(re.findall(r"[a-zA-Z]{4,}", candidate.text.lower()))
        values = set(re.findall(r"\b\d+(?:\.\d+)?\b", candidate.text))
        shared_terms = question_terms & terms
        if shared_terms and values:
            evidence.append((candidate.document_id, shared_terms, values))
    for index, (document_id, terms, values) in enumerate(evidence):
        for other_document_id, other_terms, other_values in evidence[index + 1 :]:
            if document_id != other_document_id and terms & other_terms and values != other_values:
                return True
    return False


class BoundedOrchestrator:
    def __init__(
        self,
        provider: LLMProvider,
        retrieve: Callable[[str], list[HybridCandidate]],
        rank: Callable[[str, list[HybridCandidate]], list[tuple[HybridCandidate, float]]]
        | None = None,
        max_context_characters: int = MAX_CONTEXT_CHARACTERS,
    ) -> None:
        self.provider = provider
        self.retrieve = retrieve
        self.rank = rank
        self.max_context_characters = max_context_characters

    def run(self, question: str) -> OrchestrationResult:
        steps = 1
        calculation = CALCULATION_PATTERN.search(question)
        if calculation:
            result = calculate(calculation.group(1).strip())
            steps += 1
            return OrchestrationResult(
                answer=self.provider.generate(question, [], tool_result=result),
                candidates=[],
                ranked_candidates=[],
                tools_used=["calculator"],
                steps=min(steps, MAX_STEPS),
            )

        candidates = search_knowledge_base(question, self.retrieve)
        ranked_candidates = (
            self.rank(question, candidates)
            if self.rank
            else [(candidate, candidate.hybrid_score) for candidate in candidates]
        )
        steps += 1
        context: list[str] = []
        total_characters = 0
        context_truncated = False
        for candidate, _ in ranked_candidates:
            if total_characters + len(candidate.text) > self.max_context_characters:
                context_truncated = True
                break
            context.append(candidate.text)
            total_characters += len(candidate.text)
        answer = self.provider.generate(question, context)
        conflict_detected = detect_conflicting_evidence(
            question, [candidate for candidate, _ in ranked_candidates]
        )
        return OrchestrationResult(
            answer=answer,
            candidates=candidates,
            ranked_candidates=ranked_candidates,
            tools_used=["search_knowledge_base"] if candidates else [],
            steps=min(steps, MAX_STEPS),
            context_truncated=context_truncated,
            context_chunks=len(context),
            conflict_detected=conflict_detected,
        )
