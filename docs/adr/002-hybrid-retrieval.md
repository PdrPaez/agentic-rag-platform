# ADR-002 — Hybrid retrieval

## Context

Exact domain terms and semantic paraphrases are both important retrieval signals.

## Decision

Combine BM25 lexical search and dense vector search after normalizing their scores.

## Alternatives considered

BM25-only misses paraphrases; vector-only can miss exact identifiers and policy terms.

## Consequences

The pipeline has two indexes to maintain, but retrieval behavior and weighting remain inspectable and configurable.
