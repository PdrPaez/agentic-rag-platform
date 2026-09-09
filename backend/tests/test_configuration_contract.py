from pathlib import Path


def test_env_example_documents_runtime_configuration() -> None:
    env_example = Path(__file__).parents[2] / ".env.example"
    values = {
        line.split("=", 1)[0]: line.split("=", 1)[1]
        for line in env_example.read_text(encoding="utf-8").splitlines()
        if line and not line.startswith("#") and "=" in line
    }

    expected_defaults = {
        "VITE_API_BASE_URL": "/api",
        "LLM_PROVIDER": "mock",
        "LLM_TIMEOUT_SECONDS": "30",
        "MAX_UPLOAD_SIZE_BYTES": "10485760",
        "MAX_CONTEXT_CHARACTERS": "6000",
        "RETRIEVAL_CANDIDATE_COUNT": "12",
        "FINAL_CONTEXT_COUNT": "5",
        "LEXICAL_WEIGHT": "0.4",
        "VECTOR_WEIGHT": "0.6",
        "CHUNK_SIZE": "800",
        "CHUNK_OVERLAP": "150",
    }

    assert {key: values.get(key) for key in expected_defaults} == expected_defaults
