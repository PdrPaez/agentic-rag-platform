# Agentic RAG Platform

A deliberately small foundation for exploring inspectable retrieval-augmented generation workflows.

## Current scope

The repository currently provides a typed FastAPI health endpoint and a Vite React frontend shell. Retrieval, ingestion, and agent capabilities will be added as focused tasks rather than speculative infrastructure.

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

## Project structure

- `backend/` — Python API and domain code
- `frontend/` — TypeScript React application
- `docs/` — documentation for implemented architecture
- `scripts/` — local developer utilities
- `tests/` — cross-component tests when needed

## Workflow

Development follows `feature/* → dev → main` (and corresponding `fix/*`, `docs/*`, and other scoped prefixes). Commits use `[AREA][ARAG-XXX] description`.

