from collections.abc import Sequence
from typing import Protocol

from app.rag.hybrid import HybridCandidate


class Reranker(Protocol):
    def score(self, query: str, texts: Sequence[str]) -> list[float]:
        ...


class CrossEncoderReranker:
    def __init__(self, model_name: str) -> None:
        from sentence_transformers import CrossEncoder

        self._model = CrossEncoder(model_name)

    def score(self, query: str, texts: Sequence[str]) -> list[float]:
        scores = self._model.predict([(query, text) for text in texts])
        return [float(score) for score in scores]


def rerank_candidates(
    query: str, candidates: list[HybridCandidate], reranker: Reranker, limit: int = 5
) -> list[tuple[HybridCandidate, float]]:
    if limit <= 0 or not candidates:
        return []
    scores = reranker.score(query, [candidate.text for candidate in candidates])
    if len(scores) != len(candidates):
        raise ValueError("The reranker returned an unexpected number of scores")
    ranked = sorted(
        zip(candidates, scores, strict=True),
        key=lambda item: (-item[1], item[0].chunk_id),
    )
    return ranked[:limit]

