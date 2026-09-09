# Retrieval evaluation

Deterministic benchmark on the bundled corpus. Fact coverage uses normalized text matching and is not semantic factuality evaluation.

| Strategy | Hit@1 | Hit@3 | Hit@5 | Recall@5 | MRR | Fact coverage | Avg ms | P50 ms | P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BM25 | 0.88 | 0.96 | 0.96 | 0.96 | 0.92 | 0.96 | 0.45 | 0.33 | 0.55 |
| Vector | 0.56 | 0.92 | 0.96 | 0.96 | 0.73 | 0.96 | 0.53 | 0.41 | 0.70 |
| Hybrid | 0.84 | 0.96 | 0.96 | 0.96 | 0.89 | 0.96 | 1.26 | 1.10 | 1.62 |
| Hybrid + reranking | 0.84 | 0.92 | 0.96 | 0.96 | 0.89 | 0.96 | 1.26 | 1.10 | 1.62 |
