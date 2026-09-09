# Project roadmap and governing specification

The canonical implementation specification for this repository is [implementation-specification.md](implementation-specification.md).

The portfolio-quality upgrade roadmap is preserved in [master-prompt.md](master-prompt.md). It governs the quality bar, audit priorities, measurable evidence, and hardening work that follows the implementation specification. The two documents are read together: the implementation specification defines the product contract and workflow, while the master prompt defines the senior-engineering quality target.

Both documents are versioned in the repository so work can resume consistently after an interrupted agent session. Repository rules and the current user request take precedence when they intentionally change either document.

The latest user-provided master prompt is authoritative for the portfolio upgrade. When a newer attached version is supplied, update `master-prompt.md` in the same ARAG card that records the roadmap change, then continue from the first incomplete implementation or hardening card it identifies.

## Current implementation checkpoint

The repository is currently synchronized through `ARAG-174`. Recent validated hardening includes deterministic ranking tie-breaking, independent benchmark latency measurement, structured retrieval metadata, recursive trace-secret redaction, cross-platform upload path sanitization, controlled provider and demo-seed failures, refreshed evaluation artifacts, provider error correlation, explicit Qdrant lifecycle cleanup for Windows smoke runs, complete runtime configuration documentation, and a robust real HTTP smoke workflow with dynamic port allocation, bounded subprocess cleanup, calculator coverage, trace retrieval coverage, and an adversarial prompt-injection fixture. The repository now also includes the retrieval design, security model, and individually navigable architecture decision records. The existing GitHub Actions workflow covers backend, evaluation, frontend, dependency, and smoke-test quality gates without redundant pipelines, including an enforced Ruff formatting check. A complete offline-friendly `.env.example` documents the centralized runtime configuration, including the exact supported provider values, and the changelog records the recent architectural changes. The README now links directly to the real CI workflow status, surfaces the current deterministic retrieval benchmark, explains grounded answer behavior, and links the security model and ADRs. The latest backend validation reports 74 passing tests and a clean Ruff run; frontend lint and production build remain part of the promotion gate.

## Operating rule

For each meaningful task, resume from the first incomplete `ARAG-XXX` card and follow:

`card → branch from dev → implementation → validation → commit → dev`

Promote `dev` to `main` only after the specification's relevant quality checks pass. Instructions in this repository's current user request take precedence when they intentionally change the specification.

