# Retrieval evaluation

Deterministic benchmark on the bundled corpus (30 cases; 20% negative). Fact coverage uses normalized text matching and is not semantic factuality evaluation.

## Answer behavior

Abstention accuracy: 0.80; citation presence accuracy: 0.80; expected fact coverage: 1.00.

| Strategy | Hit@1 | Hit@3 | Hit@5 | Recall@5 | MRR | Fact coverage | Avg ms | P50 ms | P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BM25 | 0.77 | 0.77 | 0.77 | 0.77 | 0.77 | 0.77 | 0.88 | 0.79 | 0.85 |
| Vector | 0.53 | 0.77 | 0.80 | 0.80 | 0.65 | 0.80 | 0.09 | 0.09 | 0.10 |
| Hybrid | 0.77 | 0.80 | 0.80 | 0.80 | 0.78 | 0.80 | 1.08 | 1.07 | 1.13 |
| Hybrid + reranking | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.33 | 0.32 | 0.34 |
