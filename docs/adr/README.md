# Architecture decision records

These concise records capture decisions that are implemented in the repository and the trade-offs they preserve.

## ADR-001 — Explicit RAG pipeline

We keep ingestion, retrieval, ranking, orchestration, and provider boundaries in application code instead of adopting a high-level RAG framework. This keeps the reference implementation inspectable and avoids framework coupling.

## ADR-002 — Hybrid retrieval

BM25 and vector retrieval are combined because lexical matching handles exact domain terms while dense retrieval handles paraphrases. Scores are normalized before weighted fusion.

## ADR-003 — Candidate reranking

An optional CrossEncoder reranks a bounded candidate set. It improves inspectability and quality without making every indexed document part of an expensive model call.

## ADR-004 — SQLite plus local Qdrant

SQLite stores document metadata and chunks; local Qdrant stores vectors. This preserves restart persistence while keeping the default setup local and small.

## ADR-005 — Bounded orchestration

The agent has an explicit step limit and an allowlist containing search and calculator tools. Deterministic routing is preferred over open-ended autonomous loops.

## ADR-006 — Deterministic mock provider

The mock provider is the default for local development, tests, and CI. An OpenAI-compatible provider remains available behind the same contract for opt-in external generation.

## ADR-007 — Grounded and abstaining responses

Responses expose citations and an answer status. The system reports insufficient context or partial evidence instead of implying unsupported certainty; calculator results do not inherit retrieval citations.
