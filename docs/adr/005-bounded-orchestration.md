# ADR-005 — Bounded orchestration

## Context

Open-ended agent loops make execution cost, safety, and debugging difficult to reason about.

## Decision

Use a configurable, low-limit orchestration flow with an explicit allowlist for search and calculator tools.

## Alternatives considered

An unlimited autonomous loop could support more complex plans but would weaken predictability and safety.

## Consequences

The agent is deliberately narrow, bounded, and easy to trace; broader planning remains a post-v1 consideration.
