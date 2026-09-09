"""Run the bundled retrieval benchmark without network or model dependencies."""

from __future__ import annotations

import hashlib
import json
import math
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from app.db.models import ChunkRecord
from app.rag.hybrid import HybridCandidate, combine_results
from app.rag.lexical import LexicalIndex, tokenize
from app.rag.reranking import rerank_candidates
from app.rag.vector_store import VectorMatch

ROOT = Path(__file__).parent
TOKEN_ALIASES = {
    "database": "qdrant", "vector": "qdrant", "latency": "response", "respond": "response",
    "severity": "sev", "outage": "incident", "approval": "approvals", "merge": "merged",
    "formatting": "ruff", "formatter": "ruff", "deadline": "target", "initial": "first",
}


@dataclass(frozen=True)
class EvaluationCase:
    question: str
    expected_document: str
    expected_facts: tuple[str, ...]


@dataclass(frozen=True)
class StageResult:
    name: str
    hit_rate_at_5: float
    mean_reciprocal_rank: float


def _canonical_tokens(text: str) -> list[str]:
    return [TOKEN_ALIASES.get(token, token) for token in tokenize(text)]


class DeterministicEmbedder:
    """Small hashed embedding used so the benchmark is reproducible offline."""

    dimension = 64

    def encode(self, texts: Sequence[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            vector = [0.0] * self.dimension
            for token in _canonical_tokens(text):
                digest = hashlib.sha256(token.encode()).digest()
                index = int.from_bytes(digest[:2], "big") % self.dimension
                vector[index] += 1.0
            norm = math.sqrt(sum(value * value for value in vector)) or 1.0
            vectors.append([value / norm for value in vector])
        return vectors


class DeterministicReranker:
    def score(self, query: str, texts: Sequence[str]) -> list[float]:
        query_tokens = set(_canonical_tokens(query))
        return [sum(token in query_tokens for token in _canonical_tokens(text)) for text in texts]


def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def load_cases() -> list[EvaluationCase]:
    data = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
    if len(data) != 10:
        raise ValueError("The bundled evaluation dataset must contain exactly 10 cases")
    return [EvaluationCase(item["question"], item["expected_document"], tuple(item["expected_facts"])) for item in data]


def load_chunks() -> list[ChunkRecord]:
    chunks: list[ChunkRecord] = []
    for path in sorted((ROOT / "documents").glob("*.md")):
        chunks.append(ChunkRecord(id=path.stem, document_id=path.name, chunk_index=0, text=path.read_text(encoding="utf-8")))
    return chunks


def _vector_matches(query: str, chunks: list[ChunkRecord], embedder: DeterministicEmbedder) -> list[VectorMatch]:
    query_vector = embedder.encode([query])[0]
    vectors = embedder.encode([chunk.text for chunk in chunks])
    ranked = sorted(zip(chunks, vectors, strict=True), key=lambda pair: _cosine(query_vector, pair[1]), reverse=True)
    return [VectorMatch(chunk.id, _cosine(query_vector, vector), {"document_id": chunk.document_id, "text": chunk.text, "document_name": chunk.document_id}) for chunk, vector in ranked]


def _document_ids(items: Sequence[HybridCandidate | tuple[HybridCandidate, float] | VectorMatch]) -> list[str]:
    values = []
    for item in items:
        candidate = item[0] if isinstance(item, tuple) else item
        if isinstance(candidate, VectorMatch):
            values.append(str(candidate.payload.get("document_id", "")))
        else:
            values.append(candidate.document_id)
    return values


def _rank_of(expected: str, documents: Sequence[str]) -> int | None:
    try:
        return documents.index(expected) + 1
    except ValueError:
        return None


def evaluate() -> tuple[list[StageResult], float, float]:
    cases = load_cases()
    chunks = load_chunks()
    index = LexicalIndex()
    index.rebuild(chunks)
    embedder = DeterministicEmbedder()
    reranker = DeterministicReranker()
    stage_documents: dict[str, list[list[str]]] = {"Vector only": [], "Hybrid": [], "Hybrid + reranking": []}
    fact_coverage: list[float] = []
    latencies: list[float] = []

    for case in cases:
        started = time.perf_counter()
        lexical = index.search(case.question, limit=5)
        vectors = _vector_matches(case.question, chunks, embedder)[:5]
        hybrid = combine_results(lexical, vectors, limit=5)
        reranked = rerank_candidates(case.question, hybrid, reranker, limit=5)
        stage_documents["Vector only"].append(_document_ids(vectors))
        stage_documents["Hybrid"].append(_document_ids(hybrid))
        stage_documents["Hybrid + reranking"].append(_document_ids(reranked))
        retrieved_text = " ".join(item.text for item in hybrid)
        fact_coverage.append(sum(_canonical_tokens(fact) and " ".join(_canonical_tokens(fact)) in " ".join(_canonical_tokens(retrieved_text)) for fact in case.expected_facts) / len(case.expected_facts))
        latencies.append((time.perf_counter() - started) * 1000)

    results: list[StageResult] = []
    for name, rankings in stage_documents.items():
        ranks = [_rank_of(case.expected_document, ranking) for case, ranking in zip(cases, rankings, strict=True)]
        results.append(StageResult(name, sum(rank is not None and rank <= 5 for rank in ranks) / len(ranks), sum(1 / rank if rank else 0 for rank in ranks) / len(ranks)))
    return results, sum(fact_coverage) / len(fact_coverage), sum(latencies) / len(latencies)


def main() -> None:
    results, coverage, latency = evaluate()
    print("Retrieval Evaluation")
    for result in results:
        print(f"\n{result.name}\nHit Rate@5: {result.hit_rate_at_5:.2f}\nMRR:        {result.mean_reciprocal_rank:.2f}")
    print(f"\nExpected Fact Coverage: {coverage:.2f}\nAverage Latency: {latency:.2f} ms")
    print("Fact coverage is normalized text matching, not semantic factuality evaluation.")


if __name__ == "__main__":
    main()
