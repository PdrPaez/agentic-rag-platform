# AGENTIC RAG PLATFORM — COMPLETE IMPLEMENTATION SPECIFICATION

You are the primary software engineering agent responsible for creating, implementing, testing, documenting, versioning, and maintaining the GitHub project described below.

You are working inside an empty Git repository.

Repository slug:

`agentic-rag-platform`

Project name used in documentation:

`Agentic RAG Platform`

Build the complete project described in this specification.

Do not merely explain what should be built.

Do not stop after planning.

Do not return pseudocode.

Do not leave required functionality as TODOs.

Implement, execute, validate, fix, document, and commit the actual project.

Do not ask follow-up questions.

Where this specification intentionally leaves implementation details open, make reasonable senior-engineering decisions and continue.

The finished repository must be:

- runnable locally;
- immediately demonstrable;
- tested;
- documented;
- understandable from the source code;
- architecturally coherent;
- professionally versioned in Git;
- usable without a paid LLM API key.

---

# 1. PRIMARY ENGINEERING PRINCIPLES

The following rules are mandatory throughout the entire implementation.

Prefer:

- correctness;
- simplicity;
- explicitness;
- maintainability;
- local developer experience;
- testability;
- observability;
- understandable architecture.

Prefer boring, reliable code over clever code.

This is a local portfolio/reference application.

It is NOT a SaaS product.

Do not implement:

- authentication;
- users;
- organizations;
- tenants;
- billing;
- roles;
- permissions;
- OAuth;
- cloud deployment;
- Kubernetes;
- distributed queues;
- event buses;
- CQRS;
- microservices;
- autonomous multi-agent swarms;
- unnecessary background workers;
- fake production infrastructure.

Do not use:

- LangChain;
- LlamaIndex;
- CrewAI;
- AutoGen;
- LangGraph;
- another agent orchestration framework.

Implement the relevant RAG and agent concepts directly so the architecture is visible and understandable from the source code.

Do not introduce generic abstraction layers without a real reason.

Avoid unnecessary:

- repository patterns;
- service patterns;
- factories;
- adapters;
- interfaces;
- dependency injection layers;
- command buses;
- generic base classes.

An abstraction is justified when:

1. there are at least two concrete implementations;
2. testing clearly benefits from the abstraction;
3. the boundary represents a genuine external dependency.

Do not create complexity merely to make the project appear enterprise-grade.

The project should demonstrate senior engineering judgment through deliberate simplicity.

---

# 2. GIT AUTHORSHIP

Use the Git identity already configured in the user's environment.

Do not modify the user's global Git identity.

Do not fabricate contributors.

Do not include visible AI attribution anywhere in Git metadata.

Never add:

`Co-authored-by: ChatGPT`

`Co-authored-by: Codex`

`Generated-by: AI`

`Generated-by: Codex`

or equivalent references.

Do not mention ChatGPT, Codex, OpenAI assistants, AI generation, or automated code generation in:

- commit messages;
- commit trailers;
- branch names;
- PR metadata;
- source comments;
- repository history.

The repository history should describe the engineering work, not which tool produced it.

---

# 3. PERMANENT BRANCH STRATEGY

Create and maintain these permanent branches:

`main`

`dev`

## main

`main` represents the stable and demonstrable version of the project.

Do not implement normal development directly on `main`.

Only promote changes to `main` after the accumulated state in `dev` is coherent, tested, documented, and working.

## dev

`dev` is the primary integration branch.

All development must reach `dev` before reaching `main`.

Normal flow:

`feature/* -> dev -> main`

Bug fixes:

`fix/* -> dev -> main`

Refactors:

`refactor/* -> dev -> main`

Tests:

`test/* -> dev -> main`

Documentation:

`docs/* -> dev -> main`

Maintenance:

`chore/* -> dev -> main`

---

# 4. TASK AND CARD STANDARD

Every meaningful engineering task must use an `ARAG-XXX` identifier.

Format:

`ARAG-001`

`ARAG-002`

`ARAG-003`

and so on.

Numbers should increase sequentially.

Each card should represent one coherent piece of engineering work.

Do not create meaningless administrative cards for trivial single-line changes.

Do not combine unrelated features into one giant card.

Example cards:

`ARAG-001 Initialize repository structure`

`ARAG-002 Configure backend application`

`ARAG-003 Configure frontend application`

`ARAG-004 Add local application configuration`

`ARAG-005 Implement persistence foundation`

`ARAG-006 Implement document ingestion`

`ARAG-007 Implement document chunking`

`ARAG-008 Implement vector embedding storage`

`ARAG-009 Implement lexical retrieval`

`ARAG-010 Implement vector retrieval`

`ARAG-011 Implement hybrid ranking`

`ARAG-012 Implement CrossEncoder reranking`

`ARAG-013 Add LLM provider abstraction`

`ARAG-014 Implement bounded agent orchestration`

`ARAG-015 Add calculator tool`

`ARAG-016 Add structured RAG responses`

`ARAG-017 Add request tracing`

`ARAG-018 Add Prometheus metrics`

`ARAG-019 Implement evaluation pipeline`

`ARAG-020 Build document management UI`

`ARAG-021 Build conversational RAG interface`

`ARAG-022 Add diagnostics interface`

`ARAG-023 Add automated CI checks`

`ARAG-024 Complete architecture documentation`

This sequence is guidance, not a requirement to create empty or artificial commits.

Combine, split, or reorder cards when implementation reality makes another breakdown more coherent.

When GitHub Issues or Projects are available and practical, associate work with the corresponding card.

Do not waste time creating unnecessary project-management bureaucracy.

---

# 5. BRANCH NAMING

Create working branches from `dev`.

Use:

`feature/ARAG-XXX-short-description`

`fix/ARAG-XXX-short-description`

`refactor/ARAG-XXX-short-description`

`test/ARAG-XXX-short-description`

`docs/ARAG-XXX-short-description`

`chore/ARAG-XXX-short-description`

Examples:

`feature/ARAG-006-document-ingestion`

`feature/ARAG-011-hybrid-ranking`

`feature/ARAG-014-agent-orchestration`

`fix/ARAG-028-document-deletion-index`

`refactor/ARAG-031-retrieval-scoring`

Avoid meaningless names such as:

`changes`

`updates`

`work`

`temp`

`new-feature`

`final`

`test123`

---

# 6. COMMIT STANDARD

Every commit must use this structure:

`[AREA][ARAG-XXX] concise description`

The description must:

- be written in English;
- describe what the commit accomplishes;
- use imperative wording where practical;
- contain no more than 20 words;
- remain concise;
- avoid unnecessary punctuation;
- never mention AI.

Examples:

`[CHORE][ARAG-001] Initialize repository structure`

`[API][ARAG-002] Configure FastAPI application`

`[UI][ARAG-003] Configure React application`

`[DB][ARAG-005] Add document metadata persistence`

`[RAG][ARAG-007] Implement configurable document chunking`

`[RETRIEVAL][ARAG-009] Add BM25 lexical retrieval`

`[RETRIEVAL][ARAG-011] Implement hybrid score normalization`

`[RETRIEVAL][ARAG-012] Add CrossEncoder candidate reranking`

`[LLM][ARAG-013] Add configurable LLM providers`

`[AGENT][ARAG-014] Implement bounded tool orchestration`

`[OBS][ARAG-017] Record request execution traces`

`[EVAL][ARAG-019] Add deterministic retrieval evaluation`

Bad commit messages:

`updates`

`changes`

`fix`

`working now`

`final`

`final final`

`implemented everything`

`AI generated retrieval`

`Codex implementation`

---

# 7. APPROVED COMMIT AREA TAGS

Use one primary tag whenever possible.

`[API]`
Backend HTTP API.

`[RAG]`
General RAG pipeline behavior.

`[AGENT]`
Agent orchestration and tool execution.

`[RETRIEVAL]`
BM25, vector search, hybrid ranking, reranking.

`[LLM]`
LLM providers, prompts, structured model interaction.

`[EVAL]`
Evaluation datasets, metrics, benchmarks.

`[OBS]`
Logging, tracing, metrics, observability.

`[UI]`
Frontend and interface behavior.

`[DB]`
SQLite, Qdrant persistence, schemas.

`[INFRA]`
Environment configuration, Docker convenience, CI.

`[TEST]`
Automated tests.

`[SECURITY]`
Input validation and security mitigations.

`[FIX]`
Bug fixes spanning several areas.

`[REFACTOR]`
Internal restructuring without intended behavioral changes.

`[DOCS]`
Documentation.

`[CHORE]`
Repository maintenance or tooling.

Do not invent new tags unless a genuinely new project area appears.

---

# 8. INCREMENTAL DEVELOPMENT RULE

Do not generate the complete repository first and commit everything afterward.

Develop incrementally.

The expected conceptual progression is approximately:

repository foundation

-> backend foundation

-> persistence

-> ingestion

-> chunking

-> embeddings

-> lexical retrieval

-> vector retrieval

-> hybrid ranking

-> reranking

-> LLM providers

-> tools

-> agent orchestration

-> structured responses

-> observability

-> evaluation

-> frontend

-> CI

-> final documentation

Each major subsystem should be validated before dependent functionality is layered on top.

Do not create artificial commits merely to simulate development history.

Every commit must represent real coherent work.

---

# 9. DEVELOPMENT WORKFLOW

For every card:

1. synchronize `dev`;
2. identify the `ARAG-XXX` task;
3. create the appropriate branch from `dev`;
4. implement only the intended scope;
5. add or update meaningful tests;
6. run relevant validation;
7. review the changed files;
8. remove debug artifacts;
9. verify no secrets are tracked;
10. update documentation when required;
11. inspect the final Git diff;
12. commit using the required format;
13. integrate the completed branch into `dev`;
14. remove obsolete local branches when safe.

Do not implement normal feature work directly on `main`.

---

# 10. TECH STACK

## Backend

Use:

- Python 3.12+
- FastAPI
- Pydantic v2
- SQLAlchemy
- SQLite
- qdrant-client local persistent mode
- sentence-transformers
- rank-bm25
- sentence-transformers CrossEncoder
- pytest
- ruff
- structured logging
- prometheus-client
- pypdf

Do not require a separate Qdrant server.

Do not require Docker to run Qdrant.

Use Qdrant embedded/local persistent mode through `qdrant-client`.

## Frontend

Use:

- React
- TypeScript
- Vite
- Tailwind CSS
- native Fetch API

Do not use:

- Redux;
- large UI component frameworks;
- unnecessary state management libraries.

## LLM

Implement:

1. deterministic local Mock provider;
2. OpenAI-compatible provider.

The Mock provider must be enabled by default.

The complete application must work without an external API key.

External LLM access is optional.

---

# 11. DEFAULT MODELS

Use a small practical embedding model by default:

`sentence-transformers/all-MiniLM-L6-v2`

Use a small practical CrossEncoder reranker by default:

`cross-encoder/ms-marco-MiniLM-L-6-v2`

Both model identifiers must remain configurable.

Avoid downloading unnecessarily large models.

Local execution should remain practical on a normal development computer.

---

# 12. APPLICATION GOAL

Build a small but production-minded Agentic RAG reference application demonstrating:

- document ingestion;
- chunking;
- embeddings;
- vector retrieval;
- lexical retrieval;
- hybrid retrieval;
- score normalization;
- reranking;
- agent tool use;
- structured outputs;
- source citations;
- deterministic evaluation;
- retrieval benchmarking;
- request tracing;
- latency measurements;
- Prometheus metrics;
- provider abstraction.

The result should look like something designed by an AI Solutions Architect.

It must not look like a generic chatbot tutorial.

The engineering architecture matters as much as the user interface.

---

# 13. CONCEPTUAL ARCHITECTURE

Use this conceptual flow:

```text
React UI
   |
   v
FastAPI
   |
   v
Agent Orchestrator
   |
   +---- Knowledge Retrieval
   |        |
   |        +---- BM25
   |        +---- Vector Search
   |        +---- Score Normalization
   |        +---- Hybrid Ranking
   |        +---- CrossEncoder Reranking
   |
   +---- Tools
   |        |
   |        +---- Calculator
   |        +---- Knowledge Search
   |
   +---- LLM Gateway
            |
            +---- Mock Provider
            +---- OpenAI-compatible Provider
```

Keep the Agent Orchestrator deliberately simple.

Do not build a multi-agent swarm.

Do not add planners, supervisors, workers, delegation graphs, or autonomous background agents.

---

# 14. AGENT BEHAVIOR

Implement a bounded orchestration loop.

Maximum:

`3 steps`

The agent may:

1. search the knowledge base;
2. use the calculator;
3. produce a final answer.

The orchestrator must never enter an unbounded loop.

The number of orchestration steps must be explicitly bounded in code.

The behavior should remain easy to understand from the implementation.

Do not simulate complex autonomous reasoning.

This project demonstrates controlled tool orchestration, not artificial autonomy.

---

# 15. LLM PROVIDER ABSTRACTION

Create one minimal provider boundary.

This abstraction is justified because there are two concrete implementations.

Prefer a small Python `Protocol`, abstract base class, or similarly lightweight contract.

Do not build a large provider framework.

Implement:

`MockLLMProvider`

`OpenAICompatibleProvider`

The provider contract should expose only the functionality the application actually needs.

---

# 16. MOCK LLM PROVIDER

The Mock provider must:

- require no network;
- require no credentials;
- behave deterministically;
- support the bundled demo documents;
- work in automated tests;
- allow the entire architecture to execute end-to-end.

Do not simply return:

`"This is a mock answer."`

Do not use one static canned response.

For knowledge questions, construct a deterministic answer from the retrieved context using simple rules.

The answer must contain information derived from selected context so that citations remain meaningful.

For calculator requests, the provider/orchestrator path must cooperate correctly with the calculator tool.

Do not attempt to make the Mock provider imitate general intelligence.

Its purpose is to make the architecture demonstrable offline.

---

# 17. OPENAI-COMPATIBLE PROVIDER

Implement a minimal OpenAI-compatible provider.

Activate it only when configuration requests it.

Use environment variables.

Do not make external API access mandatory.

Do not hardcode API keys.

Do not make network calls when the Mock provider is selected.

The provider should support configurable:

- API key;
- model;
- optional compatible base URL when useful.

Do not introduce several provider implementations in the initial project.

---

# 18. STRUCTURED RESPONSE

The backend chat response must use a Pydantic model.

Use a structure conceptually equivalent to:

```json
{
  "answer": "...",
  "citations": [
    {
      "document_id": "...",
      "document_name": "...",
      "chunk_id": "...",
      "excerpt": "..."
    }
  ],
  "tools_used": [],
  "diagnostics": {
    "request_id": "...",
    "retrieved_chunks": 0,
    "reranked_chunks": 0,
    "total_latency_ms": 0,
    "retrieval_latency_ms": 0,
    "reranking_latency_ms": 0,
    "generation_latency_ms": 0,
    "provider": "...",
    "estimated_input_tokens": 0,
    "estimated_output_tokens": 0,
    "retrieval": [
      {
        "chunk_id": "...",
        "document_name": "...",
        "bm25_score": 0.0,
        "vector_score": 0.0,
        "hybrid_score": 0.0,
        "reranker_score": 0.0
      }
    ]
  }
}
```

Exact naming may vary slightly if there is a clear technical reason.

Keep the API contract typed and stable.

Do not leak internal database objects directly through API responses.

---

# 19. CITATIONS

Answers based on knowledge retrieval must provide citations.

Each citation must contain enough information for the user to understand the source:

- document ID;
- document name;
- chunk ID;
- useful excerpt.

Citations must correspond to actual chunks used as context.

Do not invent citations.

Do not cite documents that were not selected into the final context merely to increase citation counts.

---

# 20. DOCUMENT INGESTION

Support:

- `.txt`
- `.md`
- `.pdf`

Use `pypdf` for basic PDF text extraction.

Do not implement OCR.

Reject unsupported file types cleanly.

Handle extraction failures with clear errors.

Store document metadata in SQLite.

Store chunk embeddings in Qdrant local persistent storage.

Chunking defaults:

approximately:

`800 characters`

with approximately:

`150 characters overlap`

Make these values configurable.

Chunks must retain:

- document ID;
- document name;
- chunk ID;
- chunk index;
- raw text.

Avoid silently accepting empty extracted documents.

---

# 21. DOCUMENT PERSISTENCE

SQLite should persist application metadata.

Persist enough chunk information to reconstruct lexical retrieval after application restart.

Do not depend exclusively on in-memory state for persistent documents.

At minimum, persisted data should allow the application to reconstruct:

- document identity;
- document metadata;
- chunk identity;
- chunk ordering;
- raw chunk text.

Qdrant remains responsible for vector storage.

Avoid duplicating large derived data unnecessarily.

---

# 22. PERSISTENCE CONSISTENCY

Retrieval state must remain consistent after:

- application restart;
- document ingestion;
- document deletion;
- demo reseeding.

The BM25 lexical index must be reconstructed from persisted data when needed.

Do not design the lexical search system so that it only works until FastAPI restarts.

A restart must not silently produce this invalid state:

- documents present in SQLite;
- vectors present in Qdrant;
- lexical index empty.

Synchronize persisted and in-memory retrieval state cleanly.

---

# 23. DOCUMENT DELETION

Implement:

`DELETE /api/documents/{document_id}`

Deleting a document must remove all relevant application state.

Remove:

- SQLite document metadata;
- persisted chunks;
- associated Qdrant vectors;
- associated lexical retrieval entries.

After deletion, the document must not appear in subsequent retrieval results.

Document deletion should be safe when the document does not exist.

Return an appropriate HTTP response.

---

# 24. RETRIEVAL PIPELINE

Implement actual hybrid retrieval.

Required pipeline:

```text
query
  |
  +-> BM25 search
  |
  +-> vector similarity search
  |
  v
normalize scores
  |
  v
combine scores
  |
  v
top candidate selection
  |
  v
CrossEncoder reranking
  |
  v
final context
```

Do not simply concatenate BM25 results with vector results.

Do not pretend hybrid retrieval exists by alternating results from both lists.

Implement explicit score normalization and score combination.

Put important scoring behavior into small readable functions that can be unit tested independently.

---

# 25. RETRIEVAL DEFAULTS

Default candidate retrieval:

`12`

Default final reranked context:

`5`

Make these configurable through the settings module and/or environment variables.

Keep configuration centralized.

Recommended configuration includes:

- retrieval candidate count;
- final rerank count;
- lexical/vector weighting;
- embedding model;
- reranker model;
- chunk size;
- chunk overlap.

Do not expose dozens of tuning parameters unnecessarily.

---

# 26. SCORE NORMALIZATION

Implement a clear normalization strategy.

It must handle edge cases such as:

- identical scores;
- empty result sets;
- single result;
- zero-valued ranges.

Do not allow division-by-zero behavior.

The normalization functions must be unit tested.

The implementation should be understandable without reading a research paper.

---

# 27. HYBRID RANKING

Combine normalized lexical and semantic scores.

Use explicit configurable weights.

A reasonable default is acceptable.

Do not bury ranking formulas inside a large method.

Keep the calculation separately testable.

Each candidate should retain enough diagnostic information to report:

- BM25 score;
- vector score;
- normalized values when useful;
- combined hybrid score;
- reranker score.

---

# 28. RERANKING

Use:

`cross-encoder/ms-marco-MiniLM-L-6-v2`

by default.

Apply the CrossEncoder only to the candidate shortlist, not the entire corpus.

Reranking should produce the final selected context.

Keep the reranking integration replaceable without inventing a large abstraction framework.

Tests should verify integration behavior without requiring fragile assumptions about exact floating-point model outputs when avoidable.

---

# 29. TOOLS

Implement exactly two agent tools:

1. `search_knowledge_base`
2. `calculator`

Do not introduce additional tools unless required to fix a genuine implementation problem.

The agent response must report which tools were used.

---

# 30. CALCULATOR

The calculator must safely support basic arithmetic.

Support:

- addition;
- subtraction;
- multiplication;
- division;
- modulo;
- exponentiation;
- parentheses;
- signed numeric values.

Never call Python `eval()` directly on arbitrary strings.

Prefer parsing using Python AST and explicitly allow only safe numerical expression nodes.

Reject:

- identifiers;
- variables;
- function calls;
- imports;
- attribute access;
- indexing;
- arbitrary Python syntax.

Apply reasonable input length and complexity limits.

Handle division by zero cleanly.

Write security-oriented tests for invalid calculator input.

---

# 31. OBSERVABILITY

Implement lightweight internal observability.

Do not require external services.

Implement:

- request IDs;
- structured logs;
- stage latency measurements;
- Prometheus metrics;
- internal request traces.

Do not add:

- Jaeger;
- Grafana;
- Elasticsearch;
- external tracing infrastructure;
- OpenTelemetry collectors.

The purpose is to demonstrate observability concepts without infrastructure overhead.

---

# 32. STRUCTURED LOGGING

Logs should include useful structured fields such as:

- timestamp;
- log level;
- request ID;
- operation;
- duration;
- provider;
- error category when relevant.

Do not log:

- API keys;
- secrets;
- complete private documents;
- unnecessarily large prompts;
- raw environment variables.

---

# 33. REQUEST TRACING

For every chat request, record stages such as:

`request_received`

`retrieval_started`

`retrieval_completed`

`reranking_completed`

`tool_called`

`generation_started`

`generation_completed`

Each trace entry should contain useful information such as:

- stage;
- timestamp;
- elapsed time;
- relevant lightweight metadata.

Expose:

`GET /api/traces/{request_id}`

Return the trace associated with that request.

If no trace exists, return an appropriate HTTP error.

Do not create an external tracing dependency.

---

# 34. PROMETHEUS METRICS

Expose:

`GET /metrics`

At minimum include metrics for:

- request count;
- request latency;
- retrieval latency;
- generation latency;
- document ingestion count;
- errors.

Use conventional metric types appropriately:

- counters;
- histograms;
- gauges only where actually meaningful.

Do not create dozens of vanity metrics.

---

# 35. API

Implement at least:

`GET /health`

`GET /api/documents`

`POST /api/documents`

`DELETE /api/documents/{document_id}`

`POST /api/chat`

`GET /api/traces/{request_id}`

`POST /api/demo/seed`

`GET /metrics`

Use appropriate status codes.

Use typed request/response schemas.

Return useful errors without exposing stack traces.

---

# 36. HEALTH ENDPOINT

`GET /health`

should be lightweight.

It should demonstrate that the API process is functioning.

Do not perform expensive embedding/model inference for every health check.

A simple structured response is sufficient.

Example concept:

```json
{
  "status": "ok"
}
```

---

# 37. DEMO SEEDING

Create bundled demo documents inside the repository.

Expose:

`POST /api/demo/seed`

This endpoint must ingest the bundled sample documents and make the system immediately testable.

The operation must be idempotent.

Calling it multiple times must not create duplicate:

- documents;
- chunks;
- Qdrant vectors;
- BM25 entries.

Idempotency must be covered by automated tests.

---

# 38. SAMPLE DATA

Create between 4 and 6 small fictional Markdown documents representing a fictional software company.

Possible topics:

- architecture overview;
- refund and cancellation policy;
- incident response procedure;
- engineering handbook;
- product documentation;
- support procedures.

Documents must contain concrete facts that can support retrieval evaluation.

Include details such as:

- specific durations;
- system names;
- limits;
- procedures;
- responsibilities;
- configuration values;
- policy conditions.

Do not copy real company documentation.

Do not use copyrighted proprietary documentation.

Make the documents sufficiently different that BM25 and semantic retrieval have meaningful behavior.

---

# 39. EVALUATION DATASET

Create exactly 10 evaluation questions.

Store the dataset at approximately:

`backend/evaluation/dataset.json`

or another equally clear location.

Each entry must contain:

- question;
- expected document;
- expected facts.

Include a mixture of:

- straightforward keyword retrieval questions;
- questions where BM25 should perform well;
- paraphrased questions where semantic retrieval should help;
- at least one question containing multiple relevant facts.

The evaluation dataset must correspond exactly to the bundled sample documents.

Do not create evaluation questions whose answers are ambiguous.

---

# 40. EVALUATION RUNNER

Create a simple local command such as:

`python -m app.evaluation.run`

or equivalent.

The command must actually execute the retrieval pipeline against the evaluation dataset.

Report at least:

- retrieval Hit Rate@5;
- Mean Reciprocal Rank;
- expected fact coverage;
- average latency.

Do not use another LLM as a judge.

The evaluation must be deterministic enough for local runs and CI.

---

# 41. RETRIEVAL COMPARISON

The evaluation runner should compare retrieval stages where practical.

Report at least:

1. vector-only retrieval;
2. hybrid retrieval;
3. hybrid retrieval with reranking.

Example conceptual output:

```text
Retrieval Evaluation

Vector only
Hit Rate@5: 0.80
MRR:        0.71

Hybrid
Hit Rate@5: 0.90
MRR:        0.81

Hybrid + reranking
Hit Rate@5: 1.00
MRR:        0.93

Expected Fact Coverage: 0.92
Average Latency: 185 ms
```

Do not hardcode evaluation results.

Compute them.

The goal is to demonstrate whether the more sophisticated retrieval pipeline actually provides measurable value.

---

# 42. EXPECTED FACT COVERAGE

Expected fact coverage must be deterministic.

Do not use an LLM judge.

A simple normalized text matching strategy is acceptable for the bundled controlled dataset.

Document the limitations of this metric.

Do not pretend it is equivalent to semantic factuality evaluation.

---

# 43. FRONTEND GOAL

Build a polished but deliberately simple engineering interface.

The UI should communicate:

`RAG architecture / retrieval diagnostics / agent execution`

rather than:

`consumer chatbot clone`

Use Tailwind CSS.

Dark mode by default is acceptable.

Do not spend time implementing theme switching.

Avoid unnecessary animations.

Small useful transitions are acceptable.

---

# 44. FRONTEND LAYOUT

Use approximately three areas.

## LEFT PANEL

Include:

- uploaded documents;
- upload action;
- `Load demo documents` action;
- delete document action.

Display useful document metadata without clutter.

## MAIN PANEL

Include:

- question input;
- conversation history;
- generated answer;
- source citations.

Citations should be visibly associated with answers.

## DIAGNOSTICS PANEL

Use a right panel or collapsible area.

Show:

- request ID;
- provider;
- tools used;
- retrieved chunks;
- reranked chunks;
- total latency;
- retrieval latency;
- generation latency;
- estimated tokens;
- retrieval scores;
- trace timeline.

The diagnostics experience is a major part of the project's portfolio value.

Do not hide all engineering information behind developer tools.

---

# 45. FRONTEND ENGINEERING STANDARDS

Use strict TypeScript.

Avoid `any` unless unavoidable and justified.

Prefer:

- small components;
- explicit types;
- clear API boundaries;
- simple state;
- native React functionality.

Separate API access from presentation code.

Provide:

- loading states;
- empty states;
- error states;
- success states.

Do not introduce Redux.

Do not introduce a large component library.

Do not build a generalized design system.

---

# 46. BACKEND STRUCTURE

Use approximately:

```text
backend/
  app/
    api/
    agent/
    retrieval/
    llm/
    ingestion/
    observability/
    models/
    evaluation/
    database/
    config.py
    main.py
  tests/
  pyproject.toml
```

Exact placement can differ slightly when it improves clarity.

Do not create folders merely because they appear in this specification.

Only create a module when there is real code belonging there.

Do not automatically introduce generic folders named:

- `services`
- `repositories`
- `interfaces`
- `use_cases`
- `managers`
- `factories`

unless the implementation develops a concrete need.

Avoid excessive nesting.

---

# 47. FRONTEND STRUCTURE

Use approximately:

```text
frontend/
  src/
    components/
    api/
    types/
    App.tsx
  package.json
```

Additional small folders are acceptable where useful.

Do not create excessive nesting.

---

# 48. REPOSITORY STRUCTURE

Use approximately:

```text
agentic-rag-platform/
  backend/
  frontend/
  sample-data/
  docs/
    architecture.md
    retrieval.md
    decisions.md
  scripts/
  .github/
    workflows/
  .env.example
  .editorconfig
  .gitignore
  CONTRIBUTING.md
  CHANGELOG.md
  README.md
  LICENSE
```

Do not create empty placeholder directories.

Do not add useless files merely to make the repository look larger.

---

# 49. PYTHON ENGINEERING STANDARDS

Use Python 3.12+.

Use type hints consistently.

Use Pydantic models at typed application/API boundaries.

Prefer explicit imports.

Never use wildcard imports.

Use async only where it provides real benefit.

Keep functions focused.

Keep modules reasonably small.

Avoid enormous classes.

Use explicit error handling.

Centralize configuration.

Use Ruff for formatting/lint-related checks as configured.

Prefer code that can be understood without excessive comments.

---

# 50. TYPESCRIPT ENGINEERING STANDARDS

Enable strict TypeScript behavior.

Avoid implicit unsafe types.

Use explicit API models.

Do not allow backend JSON shapes to spread through the application as loosely typed objects.

Keep React components reasonably focused.

Avoid premature hooks abstractions.

Avoid global state unless truly necessary.

---

# 51. CONFIGURATION

Create:

`.env.example`

The project must work without copying `.env.example`.

Defaults must support offline execution.

Include optional configuration similar to:

```text
LLM_PROVIDER=mock
OPENAI_API_KEY=
OPENAI_MODEL=
OPENAI_BASE_URL=
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
QDRANT_PATH=./data/qdrant
DATABASE_URL=sqlite:///./data/app.db
CHUNK_SIZE=800
CHUNK_OVERLAP=150
RETRIEVAL_CANDIDATES=12
RERANK_TOP_K=5
```

Exact names may differ if consistently documented.

Do not require secret values for local execution.

---

# 52. DATA DIRECTORIES

Runtime-generated data must live under a predictable ignored location such as:

`backend/data/`

or equivalent.

Git should not track:

- SQLite runtime databases;
- Qdrant runtime files;
- caches;
- model caches;
- uploaded user files;
- generated logs.

Sample documents required for the repository demonstration must remain tracked.

---

# 53. SECURITY

Treat all external input as untrusted.

Explicitly consider:

- uploaded files;
- filenames;
- path traversal;
- unsupported file formats;
- malformed PDFs;
- prompt injection inside documents;
- tool inputs;
- calculator expressions;
- model outputs;
- secret exposure;
- excessive context;
- malicious document content.

Do not overbuild security infrastructure.

Implement proportionate safeguards for a local reference application.

Validate filenames and paths.

Do not execute document contents.

Do not give retrieved documents direct authority to execute tools.

Treat retrieved text as information, not executable instructions.

---

# 54. PROMPT INJECTION BOUNDARY

The agent must not interpret retrieved document text as system-level instructions.

Knowledge-base content is untrusted context.

When constructing LLM input, clearly separate:

- system instructions;
- user request;
- retrieved context.

Document this design decision.

Do not attempt to create a giant security framework.

A clear context boundary and tool restrictions are sufficient for this project.

---

# 55. MODEL OUTPUT VALIDATION

When using the external LLM provider:

- validate structured outputs;
- handle malformed responses;
- return controlled errors;
- do not trust arbitrary provider output.

Where structured model output is expected, use Pydantic validation or equivalent explicit validation.

Do not allow invalid model output to crash the application unnecessarily.

---

# 56. TOKEN ESTIMATION

Diagnostics should include estimated:

- input tokens;
- output tokens.

A lightweight approximation is acceptable.

Do not add a heavy dependency solely for exact token accounting unless already justified by the provider SDK.

Clearly treat these values as estimates when they are estimates.

---

# 57. TESTING PHILOSOPHY

Write tests for meaningful behavior and regression risk.

Do not write tests for trivial getters or setters.

Do not inflate test counts artificially.

A test should protect a real behavior.

Tests must remain reasonably fast.

Avoid requiring network connectivity.

Use the Mock provider for deterministic tests.

---

# 58. REQUIRED BACKEND TESTS

At minimum test:

- chunking;
- overlap behavior;
- score normalization;
- hybrid score calculation;
- empty retrieval behavior;
- vector/hybrid retrieval integration;
- reranking integration;
- calculator valid arithmetic;
- calculator unsafe syntax rejection;
- bounded agent loop;
- structured response validation;
- citations;
- document deletion consistency;
- persistence/reconstruction behavior;
- idempotent demo seeding;
- API health endpoint.

Add other tests where implementation risk justifies them.

---

# 59. RESTART CONSISTENCY TEST

Include a meaningful test or integration test proving that persisted documents remain usable after retrieval components are reconstructed.

The system should not depend on one process-lifetime BM25 index.

The test does not need to literally spawn a new OS process if reconstruction can be reliably simulated.

---

# 60. FRONTEND VALIDATION

The frontend must successfully pass:

`npm run lint`

and:

`npm run build`

Do not configure lint scripts that silently ignore serious failures.

---

# 61. BACKEND VALIDATION

The backend must successfully pass:

`pytest`

and:

`ruff check .`

or the equivalent configured Ruff command.

If formatting validation is configured, ensure it also passes.

---

# 62. CI

Create one minimal GitHub Actions workflow.

The workflow should:

- install Python;
- install backend dependencies;
- run Ruff;
- run pytest;
- install Node;
- install frontend dependencies with `npm ci`;
- run frontend lint;
- run frontend build.

Do not deploy anything.

Do not add cloud credentials.

Do not build a complex CI matrix.

One clean validation workflow is enough.

---

# 63. DOCKER

Docker must NOT be required for the primary local development path.

Docker may be included as optional convenience only if it genuinely simplifies setup.

Do not require Docker for Qdrant.

Do not make `docker compose up` the only documented way to run the application.

If Docker adds more maintenance than value, omit it.

---

# 64. README IMPORTANCE

The README is a major deliverable.

Treat it as the project's portfolio landing page.

It should begin approximately with:

```markdown
# Agentic RAG Platform

A production-oriented reference architecture for building Retrieval-Augmented Generation systems with agent tool use, hybrid retrieval, reranking, structured outputs, evaluation and end-to-end observability.

Building a RAG demo is easy.

Building one that is observable, testable, provider-independent, resilient, evaluated and maintainable is significantly harder.

This repository focuses on those engineering problems.
```

Refine wording where useful while preserving this intent.

---

# 65. README CONTENT

Include:

- clear project description;
- feature list;
- architecture overview;
- architecture Mermaid diagram;
- retrieval pipeline Mermaid diagram;
- technology stack;
- exact local setup;
- demo instructions;
- API overview;
- evaluation instructions;
- example evaluation output format;
- architecture decisions;
- limitations;
- future improvements;
- repository structure;
- testing commands.

Do not create fake screenshots.

Only include a screenshots section if real screenshots have actually been produced and are stored in the repository.

Otherwise omit the section.

---

# 66. README LOCAL EXECUTION

Document a simple backend setup similar to:

```bash
cd backend
python -m venv .venv
```

Then provide correct environment activation commands for:

## Windows PowerShell

and:

## Unix/macOS

Then:

```bash
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

The documented commands must match the real implementation.

Do not document commands you did not verify.

---

# 67. README DEMO FLOW

Document an immediate demonstration workflow.

For example:

1. start backend;
2. start frontend;
3. click `Load demo documents`;
4. inspect loaded documents;
5. ask a sample question;
6. inspect citations;
7. inspect retrieval diagnostics;
8. inspect trace timeline;
9. optionally run evaluation.

Provide 2-4 good example questions based on the actual bundled sample documents.

Do not include examples unsupported by the sample data.

---

# 68. ARCHITECTURAL DECISIONS

Include:

`## Architectural decisions`

Explain briefly:

- why FastAPI;
- why SQLite;
- why Qdrant local mode;
- why BM25 + vector hybrid retrieval;
- why CrossEncoder reranking;
- why a bounded agent loop;
- why the project avoids heavy orchestration frameworks;
- why the application works without an API key;
- why observability is implemented internally;
- why authentication and cloud infrastructure are excluded.

Keep explanations concise and technically meaningful.

---

# 69. DELIBERATE EXCLUSIONS

Include a README section:

`## What this project deliberately does not do`

Mention:

- authentication;
- multi-tenancy;
- billing;
- cloud infrastructure;
- distributed queues;
- autonomous multi-agent systems;
- Kubernetes.

Explain that these are intentionally excluded to keep the reference implementation focused on Agentic RAG engineering.

Do not frame missing features as unfinished work.

They are scope decisions.

---

# 70. ARCHITECTURE DOCUMENTATION

Create meaningful documentation under:

`docs/`

At minimum consider:

`docs/architecture.md`

`docs/retrieval.md`

`docs/decisions.md`

Only create a document when there is enough real content.

Do not create empty placeholder documents.

Architecture documentation must describe the actual implementation.

Do not document hypothetical future infrastructure as if it already exists.

Use Mermaid diagrams where useful.

---

# 71. RETRIEVAL DOCUMENTATION

`docs/retrieval.md` should explain:

- ingestion;
- chunking;
- embedding;
- BM25;
- vector similarity;
- normalization;
- hybrid scoring;
- candidate selection;
- reranking;
- final context selection.

Include enough detail that another engineer can understand the scoring pipeline.

Do not turn it into a research paper.

---

# 72. DECISION DOCUMENTATION

`docs/decisions.md` should record a small number of relevant technical decisions.

Examples:

- local Qdrant rather than external vector infrastructure;
- deterministic Mock LLM;
- bounded agent execution;
- custom orchestration instead of agent frameworks;
- hybrid retrieval;
- lightweight observability.

Avoid fake ADR bureaucracy.

A concise decision log is enough.

---

# 73. CHANGELOG

Maintain:

`CHANGELOG.md`

Use it for meaningful user-visible or architectural changes.

Suggested sections:

`Added`

`Changed`

`Fixed`

`Removed`

Do not update the changelog for every formatting change.

---

# 74. CONTRIBUTING

Create a concise:

`CONTRIBUTING.md`

Document:

- `main` / `dev` strategy;
- feature branches;
- `ARAG-XXX` cards;
- commit format;
- required validations;
- PR expectations.

Do not create a 10-page corporate contribution guide.

---

# 75. EDITOR CONFIGURATION

Create:

`.editorconfig`

Use sensible cross-platform defaults.

Do not overconfigure editors.

---

# 76. GITIGNORE

Create a complete `.gitignore` appropriate for:

- Python;
- virtual environments;
- Python caches;
- test caches;
- Ruff caches;
- SQLite runtime files;
- Qdrant runtime data;
- environment files;
- Node;
- Vite;
- build output;
- IDE noise;
- operating system noise.

Do not ignore sample data that belongs in the repository.

---

# 77. LICENSE

Use a standard permissive open-source license appropriate for a public portfolio/reference repository unless repository context indicates otherwise.

MIT is acceptable.

Do not invent custom legal language.

---

# 78. DEPENDENCY DISCIPLINE

Before adding any dependency, ask internally:

Does this library provide enough value to justify permanent maintenance?

Prefer:

- mature packages;
- widely understood libraries;
- active projects;
- small dependency surfaces.

Do not add a dependency to avoid writing five straightforward lines of code.

Remove dependencies that become unused.

---

# 79. COMMENTS

Use comments sparingly.

Comments should explain:

- why;
- constraints;
- security considerations;
- unusual behavior.

Avoid comments that merely narrate obvious code.

Bad:

```python
# Loop through documents
for document in documents:
```

Prefer readable naming instead.

---

# 80. ERROR HANDLING

Provide clear application errors for:

- unsupported file type;
- invalid document;
- empty extracted text;
- unknown document deletion;
- invalid calculator expression;
- retrieval failures;
- provider configuration errors;
- malformed provider output.

Do not expose internal stack traces through the API.

Log enough context to debug errors.

---

# 81. LOCAL MODEL BEHAVIOR

Embedding and reranker models may require their first-time model download.

Document this clearly.

The application itself must not require paid API credentials.

Do not falsely claim the project is completely offline on the first run if model weights must be downloaded.

Once required local model assets are available, the Mock LLM path should not require external inference services.

---

# 82. PERFORMANCE

Do not prematurely optimize.

However:

- load expensive models sensibly;
- do not reload embedding models per request;
- do not reload CrossEncoder per candidate;
- avoid unnecessary repeated database work;
- keep retrieval candidate counts bounded.

Simple lazy loading or application-lifetime model instances are acceptable.

Keep the implementation understandable.

---

# 83. CONCURRENCY

Do not introduce complex concurrency infrastructure.

Use FastAPI's normal execution model appropriately.

If CPU-heavy local model work must run synchronously, handle it clearly.

Do not pretend local ML inference is magically asynchronous.

Do not add Celery or background queues.

---

# 84. FILE UPLOAD LIMITS

Apply a reasonable file size limit for uploaded demo/reference documents.

Keep the limit configurable or clearly defined.

Reject oversized uploads with a useful error.

The goal is to prevent accidental memory abuse, not to build a complete enterprise upload security system.

---

# 85. DOCUMENT NAMES

Sanitize document names used for display/storage metadata.

Do not trust raw upload paths.

Never allow client-provided filenames to control arbitrary filesystem locations.

---

# 86. REPOSITORY HYGIENE

Before completing every meaningful card:

- inspect `git status`;
- inspect the diff;
- remove dead code;
- remove unused imports;
- remove debugging prints;
- remove commented-out implementations;
- remove temporary files;
- verify naming consistency;
- verify tests;
- verify relevant documentation;
- verify no secrets are tracked.

Do not commit generated runtime state.

---

# 87. MAIN PROMOTION

Promote `dev` to `main` only when the repository is demonstrably coherent.

Before promotion verify:

- backend dependencies install;
- backend starts;
- `/health` succeeds;
- pytest passes;
- Ruff passes;
- frontend dependencies install;
- frontend lint passes;
- frontend build passes;
- demo seed works;
- at least one complete question/answer path works;
- citations work;
- diagnostics work;
- README matches reality;
- no known blocking errors remain;
- no secrets are tracked.

Do not promote an intermediary broken state merely because several cards are completed.

---

# 88. PULL REQUESTS

When practical, use Pull Requests for integration.

PR title format:

`[AREA][ARAG-XXX] Short description`

Example:

`[RETRIEVAL][ARAG-011] Add hybrid retrieval scoring`

PR descriptions should remain concise.

Use approximately:

```markdown
## Summary

What changed.

## Why

Why the change exists.

## Validation

How the change was verified.

## Notes

Only relevant implementation considerations.
```

Do not create verbose corporate PR templates for trivial work.

---

# 89. NO FAKE COMPLEXITY

Never introduce infrastructure only for architectural decoration.

Examples:

Do not add Redis unless there is a real caching requirement.

Do not add Kafka merely to claim event-driven architecture.

Do not add PostgreSQL when SQLite meets the project need.

Do not add multiple LLM providers merely to increase provider count.

Do not add WebSockets unless there is a concrete functional requirement.

Do not add Kubernetes.

Do not add MCP solely because it is fashionable.

Do not add a vector database server when Qdrant local mode is sufficient.

Every component must justify its existence.

---

# 90. NO PLACEHOLDER IMPLEMENTATION

Do not leave required functionality as:

- TODO;
- FIXME;
- stub;
- pseudocode;
- placeholder response;
- fake data flow.

Do not create APIs that return hardcoded success while underlying behavior is missing.

The required end-to-end flows must actually function.

---

# 91. NO FAKE METRICS

Do not hardcode retrieval scores, latency, token counts, trace stages, or evaluation scores.

Metrics shown in the UI must come from actual execution.

Approximation is acceptable only where explicitly described as approximation, such as token estimates.

---

# 92. PORTFOLIO QUALITY

A technical reviewer inspecting this repository should be able to determine:

- how documents are ingested;
- how text is chunked;
- how embeddings are produced;
- how vector retrieval works;
- how BM25 retrieval works;
- how scores are normalized;
- how hybrid ranking works;
- how reranking works;
- how context is selected;
- how tools are selected;
- how the bounded agent loop works;
- how providers are abstracted;
- how outputs are validated;
- how citations are generated;
- how requests are traced;
- how retrieval is evaluated.

Do not hide the interesting technical parts behind third-party frameworks.

---

# 93. INITIAL REPOSITORY TASKS

Use a sequence approximately like:

```text
ARAG-001 Initialize repository structure
ARAG-002 Configure backend application
ARAG-003 Configure frontend application
ARAG-004 Add local application configuration
ARAG-005 Implement persistence foundation
ARAG-006 Implement document ingestion
ARAG-007 Implement document chunking
ARAG-008 Implement vector embedding storage
ARAG-009 Implement lexical retrieval
ARAG-010 Implement vector retrieval
ARAG-011 Implement hybrid ranking
ARAG-012 Implement CrossEncoder reranking
ARAG-013 Add LLM provider abstraction
ARAG-014 Implement bounded agent orchestration
ARAG-015 Add calculator tool
ARAG-016 Add structured RAG responses
ARAG-017 Add request tracing
ARAG-018 Add Prometheus metrics
ARAG-019 Implement evaluation pipeline
ARAG-020 Build document management UI
ARAG-021 Build conversational RAG interface
ARAG-022 Add diagnostics interface
ARAG-023 Add automated CI checks
ARAG-024 Complete architecture documentation
```

Adjust this sequence if technical dependencies require it.

Do not create all branches simultaneously.

Develop incrementally.

---

# 94. EXAMPLE INITIAL GIT HISTORY

A healthy history may eventually resemble:

```text
[CHORE][ARAG-001] Initialize repository structure
[API][ARAG-002] Configure FastAPI application
[UI][ARAG-003] Configure React application
[INFRA][ARAG-004] Add local application configuration
[DB][ARAG-005] Add persistent document metadata
[RAG][ARAG-006] Implement document ingestion
[RAG][ARAG-007] Add configurable text chunking
[DB][ARAG-008] Add persistent vector storage
[RETRIEVAL][ARAG-009] Implement BM25 lexical search
[RETRIEVAL][ARAG-010] Implement vector similarity search
[RETRIEVAL][ARAG-011] Add hybrid retrieval scoring
[RETRIEVAL][ARAG-012] Add CrossEncoder candidate reranking
[LLM][ARAG-013] Add configurable LLM providers
[AGENT][ARAG-014] Implement bounded agent orchestration
[AGENT][ARAG-015] Add safe calculator tool
[API][ARAG-016] Add structured RAG responses
[OBS][ARAG-017] Record request execution traces
[OBS][ARAG-018] Expose application metrics
[EVAL][ARAG-019] Add deterministic retrieval evaluation
[UI][ARAG-020] Add document management interface
[UI][ARAG-021] Add conversational RAG interface
[UI][ARAG-022] Add retrieval diagnostics interface
[INFRA][ARAG-023] Add continuous integration checks
[DOCS][ARAG-024] Document architecture and retrieval design
```

This is illustrative.

Do not manipulate history to match it artificially.

---

# 95. FINAL QUALITY CHECK

Before considering the repository complete:

1. install backend dependencies;
2. run backend tests;
3. run Ruff;
4. start the backend;
5. call `/health`;
6. seed demo documents;
7. verify document listing;
8. execute a RAG question;
9. verify citations;
10. verify retrieval diagnostics;
11. verify trace retrieval;
12. verify Prometheus metrics;
13. run the evaluation command;
14. test document deletion;
15. verify deleted documents disappear from retrieval;
16. restart/reconstruct retrieval state and verify persistence;
17. install frontend dependencies;
18. run frontend lint;
19. run frontend build;
20. verify frontend/API integration;
21. inspect repository for secrets;
22. inspect ignored runtime files;
23. ensure README commands exactly match actual behavior;
24. ensure no required functionality remains as TODO;
25. ensure `dev` represents a stable integrated state;
26. promote the validated state to `main`.

If a validation step fails, fix the cause and rerun the relevant checks.

Do not ignore failing tests.

Do not disable checks simply to obtain a green result.

---

# 96. DEFINITION OF DONE FOR EACH CARD

A card is complete only when:

- intended behavior is implemented;
- required tests exist;
- relevant tests pass;
- linting passes for affected code;
- obvious dead code is removed;
- documentation is updated where needed;
- no secrets are tracked;
- the diff has been reviewed;
- the change is committed using the required format;
- the completed work is integrated into `dev`.

Code generation alone does not constitute completion.

---

# 97. FINAL DEFINITION OF DONE

The complete project is done only when:

- cloning the repository is straightforward;
- setup documentation is correct;
- backend runs locally;
- frontend runs locally;
- no paid LLM key is required;
- demo documents can be loaded;
- documents can be uploaded;
- documents can be deleted;
- persisted documents survive application restart;
- BM25 retrieval works;
- vector retrieval works;
- hybrid retrieval works;
- reranking works;
- agent tool use works;
- calculator safety works;
- structured responses work;
- citations work;
- diagnostics work;
- request traces work;
- metrics work;
- evaluation works;
- tests pass;
- lint passes;
- frontend builds;
- CI configuration is valid;
- documentation describes the actual system;
- Git history follows the project standard.

---

# 98. FINAL RESPONSE AFTER IMPLEMENTATION

At the end of the complete implementation, provide a concise summary containing:

## Created

Briefly describe the major implemented areas.

## Run locally

Provide the exact commands.

## Validation

List the actual tests/checks executed and their results.

## Architecture

Briefly summarize the implemented RAG/agent flow.

## Git

State the final branches and most recent relevant card.

## Deliberate exclusions

Mention important intentionally excluded functionality.

Do not give a long narrative.

Do not claim validations were executed if they were not actually executed.

---

# 99. AUTONOMOUS DECISION-MAKING

You are expected to make normal software engineering decisions independently.

Do not stop to ask approval for:

- filenames;
- basic folder organization;
- minor naming;
- normal library configuration;
- test layout;
- straightforward refactors;
- formatting;
- lint fixes;
- standard Git operations;
- reasonable implementation details already implied by this specification.

Choose the simplest professional solution.

The specification is intentionally detailed enough for you to proceed autonomously.

---

# 100. PRIORITY ORDER

When deciding between several valid implementations, prioritize:

1. correctness;
2. clarity;
3. maintainability;
4. local developer experience;
5. testability;
6. observability;
7. security;
8. performance;
9. extensibility.

Do not optimize for line count.

Do not optimize for architectural complexity.

Do not optimize for appearing sophisticated.

Optimize for understandable engineering.

---

# 101. MANDATORY OPERATING RULE

Treat this specification as the permanent implementation and repository policy for:

`agentic-rag-platform`

For normal work:

`ARAG card -> branch from dev -> implementation -> validation -> commit -> dev`

For stable promotion:

`dev -> full validation -> main`

Commit format:

`[AREA][ARAG-XXX] concise English description`

Maximum commit description length:

`20 words`

Never bypass the area tag.

Never bypass the card identifier.

Never perform normal feature development directly on `main`.

Never add visible AI attribution to Git history.

Never introduce infrastructure without a concrete requirement.

Never replace real functionality with placeholders.

Never claim validation without executing it.

Never sacrifice comprehensibility for unnecessary abstraction.

---

# 102. START NOW

Begin by inspecting the repository and current Git state.

If necessary:

1. initialize the required repository files;
2. establish `main` and `dev`;
3. begin with `ARAG-001`;
4. create the first appropriate working branch;
5. implement incrementally;
6. validate each meaningful subsystem;
7. integrate completed cards into `dev`;
8. continue until the complete specification is implemented;
9. perform the full final quality check;
10. promote the validated result to `main`.

Do not merely describe the implementation plan.

Build the repository.
