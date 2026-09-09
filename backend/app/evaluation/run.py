"""Run the bundled retrieval benchmark without network or model dependencies."""

from __future__ import annotations

import hashlib
import json
import math
import time
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from statistics import fmean

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db.database import Base
from app.db.models import ChunkRecord
from app.rag.hybrid import HybridCandidate
from app.rag.lexical import LexicalIndex, tokenize
from app.rag.reranking import rerank_candidates
from app.rag.retriever import HybridRetriever
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
    expected_document: str | None
    expected_facts: tuple[str, ...]


@dataclass(frozen=True)
class StageResult:
    name: str
    hit_rate_at_1: float
    hit_rate_at_3: float
    hit_rate_at_5: float
    recall_at_5: float
    mean_reciprocal_rank: float
    average_latency_ms: float
    p50_latency_ms: float
    p95_latency_ms: float
    fact_coverage: float


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


class DeterministicVectorStore:
    """In-memory vector-store adapter used by CI to exercise HybridRetriever offline."""

    def __init__(self, chunks: list[ChunkRecord], embedder: DeterministicEmbedder) -> None:
        self._matches = [
            (chunk, vector) for chunk, vector in zip(chunks, embedder.encode([chunk.text for chunk in chunks]), strict=True)
        ]

    def search(self, vector: list[float], limit: int) -> list[VectorMatch]:
        ranked = sorted(self._matches, key=lambda pair: _cosine(vector, pair[1]), reverse=True)
        return [
            VectorMatch(chunk.id, _cosine(vector, candidate_vector), {"document_id": chunk.document_id, "text": chunk.text, "document_name": chunk.document_id})
            for chunk, candidate_vector in ranked[:limit]
        ]


def _cosine(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def load_cases() -> list[EvaluationCase]:
    data = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
    if len(data) != 29:
        raise ValueError("The bundled evaluation dataset must contain exactly 29 cases")
    return [EvaluationCase(item["question"], item["expected_document"], tuple(item["expected_facts"])) for item in data]


def load_chunks() -> list[ChunkRecord]:
    chunks: list[ChunkRecord] = []
    for path in sorted((ROOT / "documents").glob("*.md")):
        chunks.append(ChunkRecord(id=path.stem, document_id=path.name, chunk_index=0, text=path.read_text(encoding="utf-8")))
    return chunks


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
    if not expected:
        return None
    try:
        return documents.index(expected) + 1
    except ValueError:
        return None


def _percentile(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    index = min(len(ordered) - 1, round((len(ordered) - 1) * percentile))
    return ordered[index]


def evaluate() -> tuple[list[StageResult], float, float]:
    cases = load_cases()
    chunks = load_chunks()
    embedder = DeterministicEmbedder()
    vector_store = DeterministicVectorStore(chunks, embedder)
    retriever = HybridRetriever(embedder, vector_store, Settings(retrieval_candidate_count=5))
    reranker = DeterministicReranker()
    stage_documents: dict[str, list[list[str]]] = {"BM25": [], "Vector": [], "Hybrid": [], "Hybrid + reranking": []}
    stage_facts: dict[str, list[float]] = {name: [] for name in stage_documents}
    stage_latencies: dict[str, list[float]] = {name: [] for name in stage_documents}
    fact_coverage: list[float] = []
    latencies: list[float] = []

    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        session.add_all(chunks)
        session.commit()
        for case in cases:
            started = time.perf_counter()
            lexical = LexicalIndex()
            lexical.rebuild(chunks)
            lexical_matches = lexical.search(case.question, 5)
            stage_documents["BM25"].append([match.document_id for match in lexical_matches])
            stage_latencies["BM25"].append((time.perf_counter() - started) * 1000)
            query_vector = embedder.encode([case.question])[0]
            vectors = vector_store.search(query_vector, 5)
            stage_documents["Vector"].append(_document_ids(vectors))
            stage_latencies["Vector"].append((time.perf_counter() - started) * 1000)
            hybrid = retriever.search(case.question, session)
            reranked = rerank_candidates(case.question, hybrid, reranker, limit=5)
            stage_documents["Hybrid"].append(_document_ids(hybrid))
            stage_documents["Hybrid + reranking"].append(_document_ids(reranked))
            for name in ("Hybrid", "Hybrid + reranking"):
                stage_latencies[name].append((time.perf_counter() - started) * 1000)
            for name in stage_documents:
                texts = [chunk.text for chunk in chunks if chunk.document_id in stage_documents[name][-1]]
                corpus = " ".join(_canonical_tokens(" ".join(texts)))
                coverage = (sum(" ".join(_canonical_tokens(fact)) in corpus for fact in case.expected_facts) / len(case.expected_facts) if case.expected_facts else 0.0)
                stage_facts[name].append(coverage)
            retrieved_text = " ".join(item.text for item in hybrid)
            fact_coverage.append(sum(_canonical_tokens(fact) and " ".join(_canonical_tokens(fact)) in " ".join(_canonical_tokens(retrieved_text)) for fact in case.expected_facts) / len(case.expected_facts) if case.expected_facts else 0.0)
            latencies.append((time.perf_counter() - started) * 1000)

    results: list[StageResult] = []
    for name, rankings in stage_documents.items():
        ranks = [_rank_of(case.expected_document, ranking) for case, ranking in zip(cases, rankings, strict=True)]
        lat = stage_latencies[name]
        results.append(StageResult(name, *(sum(rank is not None and rank <= k for rank in ranks) / len(ranks) for k in (1, 3, 5)), sum(rank is not None and rank <= 5 for rank in ranks) / len(ranks), sum(1 / rank if rank else 0 for rank in ranks) / len(ranks), fmean(lat), _percentile(lat, .50), _percentile(lat, .95), fmean(stage_facts[name])))
    return results, sum(fact_coverage) / len(fact_coverage), sum(latencies) / len(latencies)


def write_artifacts(results: list[StageResult]) -> None:
    destination = ROOT.parent.parent.parent / "docs" / "evaluation"
    destination.mkdir(parents=True, exist_ok=True)
    payload = {"dataset_cases": len(load_cases()), "strategies": [result.__dict__ for result in results]}
    (destination / "latest.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Retrieval evaluation",
        "",
        "Deterministic benchmark on the bundled corpus. Fact coverage uses normalized text matching and is not semantic factuality evaluation.",
        "",
        "| Strategy | Hit@1 | Hit@3 | Hit@5 | Recall@5 | MRR | Fact coverage | Avg ms | P50 ms | P95 ms |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for result in results:
        lines.append(f"| {result.name} | {result.hit_rate_at_1:.2f} | {result.hit_rate_at_3:.2f} | {result.hit_rate_at_5:.2f} | {result.recall_at_5:.2f} | {result.mean_reciprocal_rank:.2f} | {result.fact_coverage:.2f} | {result.average_latency_ms:.2f} | {result.p50_latency_ms:.2f} | {result.p95_latency_ms:.2f} |")
    (destination / "latest.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    results, coverage, latency = evaluate()
    write_artifacts(results)
    print("Retrieval Evaluation")
    for result in results:
        print(f"\n{result.name}\nHit Rate@5: {result.hit_rate_at_5:.2f}\nMRR:        {result.mean_reciprocal_rank:.2f}")
    print(f"\nExpected Fact Coverage: {coverage:.2f}\nAverage Latency: {latency:.2f} ms")
    print("Fact coverage is normalized text matching, not semantic factuality evaluation.")


if __name__ == "__main__":
    main()
