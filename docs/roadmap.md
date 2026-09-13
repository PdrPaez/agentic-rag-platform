# Project roadmap and governing specification

The canonical implementation specification for this repository is [implementation-specification.md](implementation-specification.md).

This roadmap records the major implementation and hardening phases of the project. Detailed architectural decisions live in the ADRs and architecture documentation, while validation evidence is maintained alongside the relevant quality and evaluation documents.

## Current implementation checkpoint

The repository is currently synchronized through `ARAG-176`. Recent validated hardening includes deterministic ranking tie-breaking, independent benchmark latency measurement, structured retrieval metadata, recursive trace-secret redaction, cross-platform upload path sanitization, controlled provider and demo-seed failures, refreshed evaluation artifacts, provider error correlation, explicit Qdrant lifecycle cleanup for Windows smoke runs, complete runtime configuration documentation, a robust real HTTP smoke workflow with dynamic port allocation, bounded subprocess cleanup, calculator coverage, trace retrieval coverage, and an adversarial prompt-injection fixture. The repository now also includes the retrieval design, security model, individually navigable architecture decision records, and a clean-clone validation record. The existing GitHub Actions workflow covers backend, evaluation, frontend, dependency, and smoke-test quality gates without redundant pipelines, including an enforced Ruff formatting check. A complete offline-friendly `.env.example` documents the centralized runtime configuration, including the exact supported provider values, and the changelog records the recent architectural changes. The README now links directly to the real CI workflow status, surfaces the current deterministic retrieval benchmark, explains grounded answer behavior, links the security model and ADRs, documents clean-clone validation, and identifies the v1.0.0 release metadata. The latest backend validation reports 74 passing tests and a clean Ruff run; frontend lint and production build remain part of the promotion gate.

## Operating rule

For each meaningful task, resume from the first incomplete `ARAG-XXX` card and follow:

`card → branch from dev → implementation → validation → commit → dev`

Promote `dev` to `main` only after the specification's relevant quality checks pass. Changes to the specification should be reflected in the corresponding roadmap card and validated before promotion.

