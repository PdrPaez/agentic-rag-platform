# Agentic RAG Platform

A deliberately small foundation for exploring inspectable retrieval-augmented generation workflows.

## Current scope

The repository provides a local-first FastAPI RAG backend and a React workspace for document ingestion, hybrid retrieval, bounded tool orchestration, citations, diagnostics, metrics, and deterministic evaluation. See [docs/architecture.md](docs/architecture.md) for the implemented request flow.

## Local setup

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`; health is exposed at `/api/health`.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

### Tests

```powershell
cd backend
python -m pytest
```

### Retrieval evaluation

Run the deterministic, offline benchmark bundled with the backend:

```powershell
cd backend
python -m app.evaluation.run
```

It compares vector-only, hybrid, and hybrid-plus-reranking retrieval using Hit Rate@5,
MRR, normalized expected-fact coverage, and average latency. Fact coverage is a simple
normalized text-matching signal for this controlled dataset; it is not semantic factuality evaluation.

## Project structure

- `backend/` — Python API and domain code
- `frontend/` — TypeScript React application
- `docs/` — documentation for implemented architecture
- `scripts/` — local developer utilities
- `tests/` — cross-component tests when needed

The complete implementation roadmap and governing engineering specification is maintained in [`docs/implementation-specification.md`](docs/implementation-specification.md), with its operating summary in [`docs/roadmap.md`](docs/roadmap.md).

## Workflow

Development follows `feature/* → dev → main` (and corresponding `fix/*`, `docs/*`, and other scoped prefixes). Commits use `[AREA][ARAG-XXX] description`.
