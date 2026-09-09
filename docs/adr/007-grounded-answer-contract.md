# ADR-007 — Grounded answer contract

## Context

Returning fluent text without sufficient evidence can create false confidence in a retrieval system.

## Decision

Expose answer status, citations, partial-answer signals, and explicit abstention when evidence is insufficient. Flag detected conflicting evidence conservatively.

## Alternatives considered

Always answering would simplify the response shape but would hide uncertainty and unsupported claims.

## Consequences

Clients can distinguish answered, partial, insufficient-context, and tool-result responses and inspect the supporting chunks.
