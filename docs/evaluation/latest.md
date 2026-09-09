# Retrieval evaluation

Deterministic benchmark on the bundled corpus (30 cases; 20% negative). Fact coverage uses normalized text matching and is not semantic factuality evaluation.

## Answer behavior

Abstention accuracy: 0.80; citation presence accuracy: 0.80; expected fact coverage: 1.00.

| Strategy | Hit@1 | Hit@3 | Hit@5 | Recall@5 | MRR | Fact coverage | Avg ms | P50 ms | P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BM25 | 0.77 | 0.77 | 0.77 | 0.77 | 0.77 | 0.77 | 0.40 | 0.30 | 0.33 |
| Vector | 0.53 | 0.77 | 0.80 | 0.80 | 0.65 | 0.80 | 0.48 | 0.38 | 0.42 |
| Hybrid | 0.77 | 0.80 | 0.80 | 0.80 | 0.78 | 0.80 | 1.15 | 1.03 | 1.12 |
| Hybrid + reranking | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 0.80 | 1.15 | 1.03 | 1.13 |
