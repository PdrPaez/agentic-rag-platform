from collections.abc import Callable

from app.rag.hybrid import HybridCandidate


def search_knowledge_base(
    question: str, retrieve: Callable[[str], list[HybridCandidate]]
) -> list[HybridCandidate]:
    """Explicit boundary for the knowledge-base search tool."""
    return retrieve(question)
