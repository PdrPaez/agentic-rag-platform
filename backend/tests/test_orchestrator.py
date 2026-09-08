from collections.abc import Sequence

from app.agents.orchestrator import MAX_STEPS, BoundedOrchestrator
from app.rag.hybrid import HybridCandidate


class FakeProvider:
    def generate(self, query: str, context: Sequence[str], tool_result: str | None = None) -> str:
        return f"tool={tool_result}" if tool_result else f"context={context[0]}"


def test_orchestrator_uses_calculator_with_bounded_steps() -> None:
    orchestrator = BoundedOrchestrator(FakeProvider(), lambda _: [])

    result = orchestrator.run("Calculate 20 / 4")

    assert result.answer == "tool=5"
    assert result.tools_used == ["calculator"]
    assert result.steps <= MAX_STEPS


def test_orchestrator_searches_knowledge_for_non_calculation_questions() -> None:
    candidate = HybridCandidate("chunk", "doc", "retrieved context", 1.0, 0.0, 1.0)
    orchestrator = BoundedOrchestrator(FakeProvider(), lambda _: [candidate])

    result = orchestrator.run("Explain the context")

    assert result.answer == "context=retrieved context"
    assert result.tools_used == ["knowledge_search"]
