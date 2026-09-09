# Project roadmap and governing specification

The canonical implementation specification for this repository is [implementation-specification.md](implementation-specification.md).

The portfolio-quality upgrade roadmap is preserved in [master-prompt.md](master-prompt.md). It governs the quality bar, audit priorities, measurable evidence, and hardening work that follows the implementation specification. The two documents are read together: the implementation specification defines the product contract and workflow, while the master prompt defines the senior-engineering quality target.

Both documents are versioned in the repository so work can resume consistently after an interrupted agent session. Repository rules and the current user request take precedence when they intentionally change either document.

The latest user-provided master prompt is authoritative for the portfolio upgrade. When a newer attached version is supplied, update `master-prompt.md` in the same ARAG card that records the roadmap change, then continue from the first incomplete implementation or hardening card it identifies.

## Current implementation checkpoint

The repository is currently synchronized through `ARAG-132`. Recent validated hardening includes deterministic ranking tie-breaking, independent benchmark latency measurement, structured retrieval metadata, recursive trace-secret redaction, controlled provider and demo-seed failures, and complete runtime configuration documentation. The latest backend validation reports 71 passing tests and a clean Ruff run; frontend lint and production build remain part of the promotion gate.

## Operating rule

For each meaningful task, resume from the first incomplete `ARAG-XXX` card and follow:

`card → branch from dev → implementation → validation → commit → dev`

Promote `dev` to `main` only after the specification's relevant quality checks pass. Instructions in this repository's current user request take precedence when they intentionally change the specification.

