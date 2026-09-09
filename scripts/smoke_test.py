"""Run a real HTTP workflow against a temporary local backend process."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
HOST = "127.0.0.1"
PORT = "8010"
BASE_URL = f"http://{HOST}:{PORT}/api"


def _wait_for_backend(client: httpx.Client, process: subprocess.Popen[str]) -> None:
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("The backend process exited before becoming ready")
        try:
            if client.get(f"{BASE_URL}/health").status_code == 200:
                return
        except httpx.HTTPError:
            time.sleep(0.25)
    raise TimeoutError("The backend did not become ready within 60 seconds")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-rag-smoke-") as temporary:
        environment = os.environ.copy()
        environment.update(
            {
                "DATABASE_URL": f"sqlite:///{Path(temporary) / 'smoke.db'}",
                "VECTOR_STORAGE_PATH": str(Path(temporary) / "vectors"),
                "BACKEND_PORT": PORT,
            }
        )
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", HOST, "--port", PORT],
            cwd=BACKEND,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        try:
            with httpx.Client(timeout=30.0) as client:
                _wait_for_backend(client, process)
                seeded = client.post(f"{BASE_URL}/demo/seed")
                assert seeded.status_code == 200
                assert len(seeded.json()) == 5

                response = client.post(
                    f"{BASE_URL}/chat",
                    json={"question": "Which vector database stores document chunks?"},
                    headers={"x-request-id": "http-smoke-chat"},
                )
                assert response.status_code == 200
                body = response.json()
                assert body["citations"]
                assert body["diagnostics"]["request_id"] == "http-smoke-chat"
                assert body["diagnostics"]["reranking_latency_ms"] >= 0

                metrics = client.get(f"{BASE_URL}/metrics")
                assert metrics.status_code == 200
                assert "rag_reranking_latency_seconds" in metrics.text

                documents = client.get(f"{BASE_URL}/documents").json()
                for document in documents:
                    assert client.delete(f"{BASE_URL}/documents/{document['id']}").status_code == 204
                assert client.get(f"{BASE_URL}/documents").json() == []
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
