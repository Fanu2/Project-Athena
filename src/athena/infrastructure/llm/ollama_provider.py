"""
Ollama LLM provider.
"""

from __future__ import annotations

import httpx

from athena.domain.ai.configuration import AIConfiguration
from athena.infrastructure.llm.provider import LLMProvider


class OllamaProvider(LLMProvider):
    """LLM provider backed by an Ollama server."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        timeout: float = 120.0,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
        )

    def generate(
        self,
        prompt: str,
        configuration: AIConfiguration,
    ) -> str:
        """Generate a response using Ollama."""

        payload = {
            "model": configuration.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": configuration.temperature,
            },
        }

        try:
            response = self._client.post(
                "/api/generate",
                json=payload,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise RuntimeError(
                "Unable to communicate with the Ollama server."
            ) from exc

        data = response.json()

        result = data.get("response")

        if not isinstance(result, str):
            raise RuntimeError(
                "Invalid response received from Ollama."
            )

        return result.strip()

    def list_models(self) -> list[str]:
        """Return the names of installed Ollama models."""

        try:
            response = self._client.get("/api/tags")
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise RuntimeError(
                "Unable to retrieve installed models from the Ollama server."
            ) from exc

        data = response.json()

        models = data.get("models")

        if not isinstance(models, list):
            raise RuntimeError(
                "Invalid model list received from Ollama."
            )

        model_names: list[str] = []

        for model in models:
            if not isinstance(model, dict):
                continue

            name = model.get("name")

            if isinstance(name, str):
                model_names.append(name)

        return sorted(model_names)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "OllamaProvider":
        return self

    def __exit__(
        self,
        exc_type: object,
        exc: BaseException | None,
        traceback: object,
    ) -> None:
        self.close()