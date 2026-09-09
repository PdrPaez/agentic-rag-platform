# Atlas architecture

The Atlas API stores document chunks in Qdrant and keeps document metadata in SQLite. The retrieval service creates chunks with a maximum size of 800 characters and an overlap of 150 characters. The API exposes retrieval diagnostics for every request.
