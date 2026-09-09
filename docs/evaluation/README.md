# Evaluation workflow

The bundled benchmark is deterministic with respect to the dataset and retrieval implementation. It uses an offline hashed embedder and deterministic reranker, so CI does not need model downloads or provider credentials. The 30-case dataset contains 20% negative cases, and backend tests separately validate answer behavior: abstention correctness, citation presence, and expected-fact coverage.

Run it from the backend directory:

```powershell
python -m app.evaluation.run
```

The command writes `docs/evaluation/latest.json` and `docs/evaluation/latest.md`. Latency values are machine-dependent measurements; retrieval rankings and normalized fact labels come from the committed corpus and dataset. The benchmark is evidence for this controlled corpus, not a universal RAG quality claim.

Answer-behavior metrics are defined as follows:

- `abstention_accuracy`: the share of cases where retrieval is empty exactly when the dataset expects abstention;
- `citation_presence_accuracy`: the share of cases where retrieved evidence is present exactly when citations are expected;
- `expected_fact_coverage`: the share of expected fact labels found by normalized text matching in retrieved content.

These checks evaluate deterministic retrieval behavior and citation signals; they do not establish semantic faithfulness of generated prose.
