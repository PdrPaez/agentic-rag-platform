# Retrieval evaluation

Deterministic benchmark on the bundled corpus. Fact coverage uses normalized text matching and is not semantic factuality evaluation.

| Strategy | Hit@1 | Hit@3 | Hit@5 | Recall@5 | MRR | Fact coverage | Avg ms | P50 ms | P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BM25 | 0.73 | 0.80 | 0.80 | 0.80 | 0.77 | 0.80 | 0.42 | 0.33 | 0.38 |
| Vector | 0.47 | 0.77 | 0.80 | 0.80 | 0.61 | 0.80 | 0.51 | 0.41 | 0.46 |
| Hybrid | 0.70 | 0.80 | 0.80 | 0.80 | 0.74 | 0.80 | 1.20 | 1.10 | 1.19 |
| Hybrid + reranking | 0.70 | 0.77 | 0.80 | 0.80 | 0.74 | 0.80 | 1.20 | 1.10 | 1.19 |
