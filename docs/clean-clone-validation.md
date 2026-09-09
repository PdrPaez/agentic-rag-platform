# Clean-clone validation

The release workflow was validated from a fresh clone of the repository using a new Python virtual environment and a fresh Node installation. No personal `.env`, local database, model cache, or existing `node_modules` directory was used.

## Validated commands

- Backend editable install with development dependencies.
- `ruff check backend/app backend/tests`.
- `ruff format --check backend/app backend/tests`.
- `pytest backend/tests --cov=backend/app --cov-fail-under=85 -q`.
- `python -m app.evaluation.run`.
- `npm ci`, `npm run lint`, and `npm run build`.
- `python scripts/smoke_test.py`.
- `npm run dev -- --host 127.0.0.1 --port 4173`, verified with an HTTP 200 response.

## Results

The clean clone passed 74 backend tests, 92.94% coverage, Ruff lint and formatting, deterministic evaluation, frontend type validation, and production build. The real HTTP smoke workflow passed demo seeding, retrieval, calculator routing, trace retrieval, metrics, and document deletion. The frontend development server started successfully and served the application with HTTP 200.

The smoke test initially exposed a Windows file-lock cleanup issue in local Qdrant storage. ARAG-174 added explicit vector-store lifecycle cleanup; the smoke test passed from a fresh clone after that fix.
