# Retrieval evaluation

Deterministic benchmark on the bundled corpus. Fact coverage uses normalized text matching and is not semantic factuality evaluation.

| Strategy | Hit@1 | Hit@3 | Hit@5 | Recall@5 | MRR | Fact coverage | Avg ms | P50 ms | P95 ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BM25 | 0.88 | 0.96 | 0.96 | 0.96 | 0.92 | 0.96 | 0.44 | 0.33 | 0.36 |
| Vector | 0.56 | 0.92 | 0.96 | 0.96 | 0.73 | 0.96 | 0.52 | 0.41 | 0.45 |
| Hybrid | 0.84 | 0.96 | 0.96 | 0.96 | 0.89 | 0.96 | 1.22 | 1.10 | 1.19 |
| Hybrid + reranking | 0.84 | 0.92 | 0.96 | 0.96 | 0.89 | 0.96 | 1.22 | 1.10 | 1.19 |
