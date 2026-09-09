# ADR-004 — SQLite plus local Qdrant

## Context

The platform must persist locally across restarts without requiring a managed service.

## Decision

Use SQLite for document metadata and chunks, and local Qdrant storage for vectors.

## Alternatives considered

Hosted databases and vector services would add credentials and infrastructure to the default workflow.

## Consequences

Setup stays small and reproducible, while production deployments will need a managed persistence strategy.
