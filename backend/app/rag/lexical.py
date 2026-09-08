import re
from dataclasses import dataclass

from rank_bm25 import BM25Okapi

from app.db.models import ChunkRecord

TOKEN_PATTERN = re.compile(r"\w+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


@dataclass(frozen=True)
class LexicalMatch:
    chunk_id: str
    score: float
    text: str
    document_id: str


class LexicalIndex:
    def __init__(self) -> None:
        self._chunk_ids: list[str] = []
        self._chunks: list[ChunkRecord] = []
        self._index: BM25Okapi | None = None

    def rebuild(self, chunks: list[ChunkRecord]) -> None:
        self._chunks = list(chunks)
        self._chunk_ids = [chunk.id for chunk in self._chunks]
        self._index = BM25Okapi([tokenize(chunk.text) for chunk in self._chunks]) if chunks else None

    def search(self, query: str, limit: int = 12) -> list[LexicalMatch]:
        if self._index is None or limit <= 0 or not query.strip():
            return []
        scores = self._index.get_scores(tokenize(query))
        ranked_indexes = sorted(range(len(scores)), key=lambda index: scores[index], reverse=True)
        query_tokens = set(tokenize(query))
        return [
            LexicalMatch(
                chunk_id=self._chunk_ids[index],
                score=float(scores[index]),
                text=self._chunks[index].text,
                document_id=self._chunks[index].document_id,
            )
            for index in ranked_indexes[:limit]
            if query_tokens.intersection(tokenize(self._chunks[index].text))
        ]

