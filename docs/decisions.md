# Technical decision log

## Local persistence

SQLite stores document metadata and chunks while local Qdrant stores embeddings. This preserves restart behavior without requiring external infrastructure.

## Explicit hybrid pipeline

BM25 handles exact domain terminology and dense vectors handle semantic variation. Min-max normalization and configurable weights make the fusion inspectable.

## Bounded orchestration

Custom orchestration is used instead of an agent framework. Search and calculator are explicit allowlisted tools, and the step limit prevents unbounded execution.

## Deterministic default provider

The Mock provider is the default for offline development and CI. An OpenAI-compatible provider can be selected explicitly when external generation is appropriate.

## Lightweight observability

Request IDs, in-process traces, Prometheus metrics, and structured diagnostics provide operational visibility without introducing a distributed telemetry stack.
