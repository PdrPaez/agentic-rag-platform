import re
from collections.abc import Callable
from dataclasses import dataclass

from app.agents.tools.calculator import calculate
from app.agents.tools.search import search_knowledge_base
from app.llm.providers import LLMProvider
from app.rag.hybrid import HybridCandidate

MAX_STEPS = 3
MAX_CONTEXT_CHARACTERS = 6000
CALCULATION_PATTERN = re.compile(r"(?:calculate|compute|what is)\s+([0-9+\-*/().% ]+?)[?!.]*$", re.IGNORECASE)


@dataclass(frozen=True)
class OrchestrationResult:
    answer: str
    candidates: list[HybridCandidate]
    ranked_candidates: list[tuple[HybridCandidate, float]]
    tools_used: list[str]
    steps: int


class BoundedOrchestrator:
    def __init__(
        self,
        provider: LLMProvider,
        retrieve: Callable[[str], list[HybridCandidate]],
        rank: Callable[[str, list[HybridCandidate]], list[tuple[HybridCandidate, float]]] | None = None,
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
        ranked_candidates = self.rank(question, candidates) if self.rank else [
            (candidate, candidate.hybrid_score) for candidate in candidates
        ]
        steps += 1
        context: list[str] = []
        total_characters = 0
        for candidate, _ in ranked_candidates:
            if total_characters + len(candidate.text) > self.max_context_characters:
                break
            context.append(candidate.text)
            total_characters += len(candidate.text)
        answer = self.provider.generate(question, context)
        return OrchestrationResult(
            answer=answer,
            candidates=candidates,
            ranked_candidates=ranked_candidates,
            tools_used=["search_knowledge_base"] if candidates else [],
            steps=min(steps, MAX_STEPS),
        )

