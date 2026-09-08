from dataclasses import dataclass
from pathlib import Path
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


@dataclass(frozen=True)
class VectorMatch:
    chunk_id: str
    score: float
    payload: dict[str, Any]


class LocalVectorStore:
    def __init__(self, storage_path: str, collection_name: str) -> None:
        Path(storage_path).mkdir(parents=True, exist_ok=True)
        self.client = QdrantClient(path=storage_path)
        self.collection_name = collection_name

    def ensure_collection(self, dimension: int) -> None:
        if self.client.collection_exists(self.collection_name):
            return
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=dimension, distance=Distance.COSINE),
        )

    def upsert(self, chunk_ids: list[str], vectors: list[list[float]], payloads: list[dict[str, Any]]) -> None:
        if not chunk_ids or len(chunk_ids) != len(vectors) or len(vectors) != len(payloads):
            raise ValueError("Chunk IDs, vectors, and payloads must have matching non-zero lengths")
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(id=chunk_id, vector=vector, payload=payload)
                for chunk_id, vector, payload in zip(chunk_ids, vectors, payloads, strict=True)
            ],
        )

    def search(self, vector: list[float], limit: int) -> list[VectorMatch]:
        if limit <= 0:
            return []
        results = self.client.query_points(
            collection_name=self.collection_name, query=vector, limit=limit, with_payload=True
        ).points
        return [
            VectorMatch(chunk_id=str(result.id), score=result.score, payload=result.payload or {})
            for result in results
        ]

    def delete_document(self, document_id: str) -> None:
        from qdrant_client.models import FieldCondition, Filter, MatchValue

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[FieldCondition(key="document_id", match=MatchValue(value=document_id))]
            ),
        )

