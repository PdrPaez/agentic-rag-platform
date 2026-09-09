# Changelog

## [1.0.0]

### Added

- Initial repository structure for the Agentic RAG Platform.
- FastAPI document ingestion, persistence, hybrid retrieval, reranking, bounded orchestration, citations, request observability, metrics, and deterministic evaluation.
- React document management, conversational retrieval, and diagnostics workspace.
- Automated backend and frontend validation through GitHub Actions.

### Changed

- Added deterministic ranking tie-breaking, structured retrieval diagnostics, and independent benchmark latency measurement.
- Hardened upload validation, provider and demo-seed failure handling, request correlation, trace redaction, and document deletion consistency.
- Added retrieval and technical decision documentation, a complete environment template, and enforced Python formatting in CI.

### Fixed

- Added explicit local vector-store shutdown cleanup so Windows smoke validation releases temporary storage correctly.

### Security

- Added adversarial retrieval coverage and documented prompt-injection, tool, upload, and secret-handling boundaries.

## Unreleased
