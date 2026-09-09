# Evaluation workflow

The bundled benchmark is deterministic with respect to the dataset and retrieval implementation. It uses an offline hashed embedder and deterministic reranker, so CI does not need model downloads or provider credentials.

Run it from the backend directory:

```powershell
python -m app.evaluation.run
```

The command writes `docs/evaluation/latest.json` and `docs/evaluation/latest.md`. Latency values are machine-dependent measurements; retrieval rankings and normalized fact labels come from the committed corpus and dataset. The benchmark is evidence for this controlled corpus, not a universal RAG quality claim.
