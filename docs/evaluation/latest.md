# Retrieval evaluation

Deterministic benchmark on the bundled corpus (30 cases; 20% negative). Fact coverage uses normalized text matching and is not semantic factuality evaluation.

## Answer behavior

Abstention accuracy: 0.80; citation presence accuracy: 0.80; expected fact coverage: 1.00.

| Strategy | Hit@1 | Hit@3 | Hit@5 | Recall@5 | MRR | Fact coverage | Avg ms | P50 ms | P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BM25 | 0.73 | 0.80 | 0.80 | 0.80 | 0.77 | 0.80 | 0.43 | 0.33 | 0.37 |
| Vector | 0.47 | 0.77 | 0.80 | 0.80 | 0.61 | 0.80 | 0.52 | 0.41 | 0.46 |
| Hybrid | 0.70 | 0.80 | 0.80 | 0.80 | 0.74 | 0.80 | 1.21 | 1.09 | 1.20 |
| Hybrid + reranking | 0.70 | 0.77 | 0.80 | 0.80 | 0.74 | 0.80 | 1.21 | 1.09 | 1.20 |
