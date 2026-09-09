from __future__ import annotations

import logging
import re
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
SENSITIVE_METADATA_KEYS = {"api_key", "authorization", "password", "secret", "token"}


def _is_sensitive_key(key: object) -> bool:
    normalized = re.sub(r"[^a-z0-9]", "", str(key).lower())
    return any(
        marker in normalized for marker in ("apikey", "authorization", "password", "secret")
    ) or normalized.endswith("token")


def _safe_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: "[REDACTED]" if _is_sensitive_key(key) else _safe_value(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_safe_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_safe_value(item) for item in value)
    return value


def _safe_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
    return _safe_value(metadata)


def record_trace(request_id: str, stage: str, elapsed_ms: float, **metadata: Any) -> None:
    safe_metadata = _safe_metadata(metadata)
    entry = TraceEntry(stage, datetime.now(UTC).isoformat(), round(elapsed_ms, 3), safe_metadata)
    with _lock:
        _traces.setdefault(request_id, []).append(entry)
    logger.info(
        "trace_stage",
        extra={
            "request_id": request_id,
            "stage": stage,
            "elapsed_ms": entry.elapsed_ms,
            **safe_metadata,
        },
    )


def get_trace(request_id: str) -> list[dict[str, Any]] | None:
    with _lock:
        entries = _traces.get(request_id)
        return [asdict(entry) for entry in entries] if entries is not None else None
