# ADR-003 — CrossEncoder reranking

## Context

Initial retrieval is fast but benefits from a more precise relevance judgment on a small candidate set.

## Decision

Optionally rerank the bounded hybrid candidate pool with a CrossEncoder.

## Alternatives considered

Reranking every indexed chunk would increase latency and model cost; omitting reranking reduces relevance precision.

## Consequences

Quality can improve at a bounded latency cost, and diagnostics expose the reranking stage and scores.
