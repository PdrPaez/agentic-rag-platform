# ADR-006 — Deterministic mock provider

## Context

Local development and CI must work without paid accounts, network calls, or nondeterministic generation.

## Decision

Make the deterministic mock provider the default and keep the OpenAI-compatible provider opt-in behind the same contract.

## Alternatives considered

Requiring an external model would make validation slower, cost-bearing, and less reproducible.

## Consequences

The full workflow is testable offline; production users must choose and configure a real provider for model quality.
