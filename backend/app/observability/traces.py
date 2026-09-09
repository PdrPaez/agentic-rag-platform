from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from threading import Lock
from typing import Any


@dataclass(frozen=True)
class TraceEntry:
    stage: str
    timestamp: str
    elapsed_ms: float
    metadata: dict[str, Any]


_traces: dict[str, list[TraceEntry]] = {}
_lock = Lock()
logger = logging.getLogger("agentic_rag_platform")


def record_trace(request_id: str, stage: str, elapsed_ms: float, **metadata: Any) -> None:
    entry = TraceEntry(stage, datetime.now(UTC).isoformat(), round(elapsed_ms, 3), metadata)
    with _lock:
        _traces.setdefault(request_id, []).append(entry)
    logger.info("trace_stage", extra={"request_id": request_id, "stage": stage, "elapsed_ms": entry.elapsed_ms, **metadata})


def get_trace(request_id: str) -> list[dict[str, Any]] | None:
    with _lock:
        entries = _traces.get(request_id)
        return [asdict(entry) for entry in entries] if entries is not None else None
