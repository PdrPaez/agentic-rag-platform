# Retrieval evaluation

Deterministic benchmark on the bundled corpus. Fact coverage uses normalized text matching and is not semantic factuality evaluation.

| Strategy | Hit@1 | Hit@3 | Hit@5 | Recall@5 | MRR | Fact coverage | Avg ms | P50 ms | P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BM25 | 0.76 | 0.83 | 0.83 | 0.83 | 0.79 | 0.83 | 0.42 | 0.33 | 0.38 |
| Vector | 0.48 | 0.79 | 0.83 | 0.83 | 0.63 | 0.83 | 0.51 | 0.41 | 0.46 |
| Hybrid | 0.72 | 0.83 | 0.83 | 0.83 | 0.77 | 0.83 | 1.20 | 1.10 | 1.19 |
| Hybrid + reranking | 0.72 | 0.79 | 0.83 | 0.83 | 0.77 | 0.83 | 1.20 | 1.10 | 1.19 |
