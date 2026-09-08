from collections.abc import Sequence
from typing import Protocol

import httpx


class LLMProvider(Protocol):
    name: str

    def generate(self, query: str, context: Sequence[str], tool_result: str | None = None) -> str:
        ...


class MockLLMProvider:
    name = "mock"

    def generate(self, query: str, context: Sequence[str], tool_result: str | None = None) -> str:
        if tool_result is not None:
            return f"The calculator result is {tool_result}."
        if not context:
            return "I could not find relevant information in the knowledge base."
        excerpt = " ".join(context[:2]).strip()
        return f"Based on the knowledge base: {excerpt}"


class OpenAICompatibleProvider:
    name = "openai-compatible"

    def __init__(self, api_key: str, model_name: str, base_url: str) -> None:
        if not api_key:
            raise ValueError("LLM_API_KEY is required for the OpenAI-compatible provider")
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")

    def generate(self, query: str, context: Sequence[str], tool_result: str | None = None) -> str:
        prompt = "\n\n".join(context)
        if tool_result is not None:
            prompt = f"Calculator result: {tool_result}\n\n{prompt}"
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "Answer using only the supplied context."},
                    {"role": "user", "content": f"Context:\n{prompt}\n\nQuestion: {query}"},
                ],
            },
            timeout=30.0,
        )
        response.raise_for_status()
        data = response.json()
        try:
            return str(data["choices"][0]["message"]["content"])
        except (KeyError, IndexError, TypeError) as exc:
            raise ValueError("The LLM provider returned an invalid response") from exc


def create_provider(provider_name: str, model_name: str, api_key: str | None, base_url: str) -> LLMProvider:
    if provider_name == "mock":
        return MockLLMProvider()
    if provider_name == "openai-compatible":
        return OpenAICompatibleProvider(api_key or "", model_name, base_url)
    raise ValueError(f"Unsupported LLM provider: {provider_name}")

