# ADR-001 — No high-level RAG framework

## Context

The core retrieval and orchestration behavior must remain inspectable for a reference implementation.

## Decision

Keep ingestion, retrieval, ranking, orchestration, and provider boundaries in application code.

## Alternatives considered

Adopting a high-level RAG framework would reduce boilerplate but hide important control flow and add coupling.

## Consequences

The project owns more integration code, but reviewers can trace behavior directly from the source.
