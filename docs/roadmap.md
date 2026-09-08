# Project roadmap and governing specification

The canonical implementation specification for this repository is [implementation-specification.md](implementation-specification.md).

It is the source of truth for project scope, architecture, engineering standards, task sequencing, validation, and Git workflow. The specification is preserved in the repository so work can resume consistently after an interrupted agent session.

## Operating rule

For each meaningful task, resume from the first incomplete `ARAG-XXX` card and follow:

`card → branch from dev → implementation → validation → commit → dev`

Promote `dev` to `main` only after the specification's relevant quality checks pass. Instructions in this repository's current user request take precedence when they intentionally change the specification.

