"""Run a real HTTP workflow against a temporary local backend process."""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
HOST = "127.0.0.1"


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind((HOST, 0))
        return int(probe.getsockname()[1])


def _wait_for_backend(client: httpx.Client, process: subprocess.Popen[str], base_url: str) -> None:
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError("The backend process exited before becoming ready")
        try:
            if client.get(f"{base_url}/health").status_code == 200:
                return
        except httpx.HTTPError:
            time.sleep(0.25)
    raise TimeoutError("The backend did not become ready within 60 seconds")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="agentic-rag-smoke-") as temporary:
        port = _free_port()
        base_url = f"http://{HOST}:{port}/api"
        environment = os.environ.copy()
        environment.update(
            {
                "DATABASE_URL": f"sqlite:///{Path(temporary) / 'smoke.db'}",
                "VECTOR_STORAGE_PATH": str(Path(temporary) / "vectors"),
                "BACKEND_PORT": str(port),
            }
        )
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", "--host", HOST, "--port", str(port)],
            cwd=BACKEND,
            env=environment,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            with httpx.Client(timeout=30.0) as client:
                _wait_for_backend(client, process, base_url)
                seeded = client.post(f"{base_url}/demo/seed")
                assert seeded.status_code == 200
                assert len(seeded.json()) == 5

                response = client.post(
                    f"{base_url}/chat",
                    json={"question": "Which vector database stores document chunks?"},
                    headers={"x-request-id": "http-smoke-chat"},
                )
                assert response.status_code == 200
                body = response.json()
                assert body["citations"]
                assert body["diagnostics"]["request_id"] == "http-smoke-chat"
                assert body["diagnostics"]["reranking_latency_ms"] >= 0

                calculation = client.post(
                    f"{base_url}/chat",
                    json={"question": "Calculate 20 / 4"},
                    headers={"x-request-id": "http-smoke-calculator"},
                )
                assert calculation.status_code == 200
                assert calculation.json()["answer_status"] == "tool_result"
                assert calculation.json()["citations"] == []

                trace = client.get(f"{base_url}/traces/http-smoke-chat")
                assert trace.status_code == 200
                assert any(entry["stage"] == "generation_completed" for entry in trace.json()["entries"])

                metrics = client.get(f"{base_url}/metrics")
                assert metrics.status_code == 200
                assert "rag_reranking_latency_seconds" in metrics.text

                documents = client.get(f"{base_url}/documents").json()
                for document in documents:
                    assert client.delete(f"{base_url}/documents/{document['id']}").status_code == 204
                assert client.get(f"{base_url}/documents").json() == []
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
