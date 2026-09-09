from dataclasses import dataclass

from app.rag.lexical import LexicalMatch
from app.rag.normalization import min_max_normalize
from app.rag.vector_store import VectorMatch


@dataclass(frozen=True)
class HybridCandidate:
    chunk_id: str
    document_id: str
    text: str
    bm25_score: float
    vector_score: float
    hybrid_score: float
    document_name: str = ""
    chunk_index: int = 0


def combine_results(
    lexical_matches: list[LexicalMatch],
    vector_matches: list[VectorMatch],
    *,
    lexical_weight: float = 0.4,
    vector_weight: float = 0.6,
    limit: int = 12,
) -> list[HybridCandidate]:
    if lexical_weight < 0 or vector_weight < 0 or lexical_weight + vector_weight == 0:
        raise ValueError("Retrieval weights must be non-negative and have a positive sum")
    if limit <= 0:
        return []

    normalized_lexical = min_max_normalize([match.score for match in lexical_matches])
    normalized_vector = min_max_normalize([match.score for match in vector_matches])
    candidates: dict[str, HybridCandidate] = {}

    for index, match in enumerate(lexical_matches):
        candidates[match.chunk_id] = HybridCandidate(
            chunk_id=match.chunk_id,
            document_id=match.document_id,
            text=match.text,
            bm25_score=normalized_lexical[index],
            vector_score=0.0,
            hybrid_score=normalized_lexical[index] * lexical_weight,
            document_name=match.document_id,
            chunk_index=match.chunk_index,
        )

    for index, match in enumerate(vector_matches):
        lexical = candidates.get(match.chunk_id)
        vector_score = normalized_vector[index]
        bm25_score = lexical.bm25_score if lexical else 0.0
        candidates[match.chunk_id] = HybridCandidate(
            chunk_id=match.chunk_id,
            document_id=str(match.payload.get("document_id", lexical.document_id if lexical else "")),
            text=str(match.payload.get("text", lexical.text if lexical else "")),
            bm25_score=bm25_score,
            vector_score=vector_score,
            hybrid_score=bm25_score * lexical_weight + vector_score * vector_weight,
            document_name=str(match.payload.get("document_name", lexical.document_name if lexical else "")),
            chunk_index=int(match.payload.get("chunk_index", lexical.chunk_index if lexical else 0)),
        )

    weight_total = lexical_weight + vector_weight
    ranked = sorted(
        candidates.values(),
        key=lambda candidate: (-candidate.hybrid_score / weight_total, candidate.chunk_id),
    )
    return ranked[:limit]

