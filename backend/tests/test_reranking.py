from collections.abc import Sequence

from app.rag.hybrid import HybridCandidate
from app.rag.reranking import rerank_candidates


class FakeReranker:
    def score(self, query: str, texts: Sequence[str]) -> list[float]:
        return [float(len(text)) for text in texts]


def test_rerank_candidates_orders_by_crossencoder_scores() -> None:
    candidates = [
        HybridCandidate("short", "doc", "small", 1.0, 0.0, 1.0),
        HybridCandidate("long", "doc", "much more useful context", 0.5, 0.5, 0.8),
    ]

    ranked = rerank_candidates("useful", candidates, FakeReranker(), limit=1)

    assert ranked[0][0].chunk_id == "long"
    assert ranked[0][1] == float(len("much more useful context"))
