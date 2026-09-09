# Retrieval pipeline

The platform keeps retrieval local and inspectable. Document ingestion extracts UTF-8 text or PDF page text, validates the extension and size, and splits the text into configurable character chunks (`CHUNK_SIZE` and `CHUNK_OVERLAP`). Each chunk retains its document ID and chunk index.

The embedding runtime encodes chunks with the configured sentence-transformer model and stores vectors plus document metadata in local Qdrant. At query time, the persisted SQLite chunks rebuild a BM25 lexical index, while the query embedding searches Qdrant for dense candidates.

BM25 and vector scores are min-max normalized independently. Hybrid scoring combines them with `LEXICAL_WEIGHT` and `VECTOR_WEIGHT`; candidates are sorted by descending weighted score with `chunk_id` as a deterministic tie-breaker. The bounded candidate pool is controlled by `RETRIEVAL_CANDIDATE_COUNT`.

The CrossEncoder reranker scores only that bounded hybrid pool. Reranked results are limited by `FINAL_CONTEXT_COUNT`, then the context budget truncates whole candidates when necessary. The selected chunks are the only retrieval evidence passed to the provider and cited in a grounded response.

The offline evaluation runner compares BM25, vector, hybrid, and hybrid-plus-reranking stages using the committed corpus and dataset. Its latency values include the measured query stage for each strategy and are machine-dependent.
