"""Run the fast HTTP workflow smoke checks from the repository root."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TESTS = [
    "tests/test_health.py",
    "tests/test_demo_seed.py",
    "tests/test_documents_api.py",
    "tests/test_chat_api.py",
]


def main() -> int:
    command = [sys.executable, "-m", "pytest", "-q", *TESTS]
    completed = subprocess.run(command, cwd=ROOT / "backend", check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
