# Retrieval evaluation

Deterministic benchmark on the bundled corpus. Fact coverage uses normalized text matching and is not semantic factuality evaluation.

| Strategy | Hit@1 | Hit@3 | Hit@5 | Recall@5 | MRR | Fact coverage | Avg ms | P50 ms | P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BM25 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.63 | 0.34 | 3.19 |
| Vector | 0.60 | 1.00 | 1.00 | 1.00 | 0.78 | 1.00 | 0.72 | 0.44 | 3.29 |
| Hybrid | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.46 | 1.15 | 4.29 |
| Hybrid + reranking | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.46 | 1.15 | 4.29 |
