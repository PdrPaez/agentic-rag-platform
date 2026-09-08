import pytest

from app.llm.providers import MockLLMProvider, create_provider


def test_mock_provider_generates_from_context_and_tool_result() -> None:
    provider = MockLLMProvider()

    assert "retrieval" in provider.generate("How?", ["Hybrid retrieval combines signals."])
    assert provider.generate("Calculate", [], tool_result="42") == "The calculator result is 42."


def test_mock_provider_is_default_and_does_not_need_credentials() -> None:
    assert create_provider("mock", "unused", None, "unused").name == "mock"


def test_openai_provider_requires_a_key() -> None:
    with pytest.raises(ValueError, match="LLM_API_KEY"):
        create_provider("openai-compatible", "model", None, "https://example.com/v1")
