"""
Ollama LLM provider.
"""

from __future__ import annotations

import requests

from athena.ai.llm.exceptions import (
    GenerationError,
    ProviderUnavailableError,
)
from athena.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)
from athena.ai.llm.provider import (
    LLMProvider,
)
from athena.settings import LLMSettings


class OllamaProvider(LLMProvider):
    """LLM provider using local Ollama server."""

    def __init__(
        self,
        settings: LLMSettings | None = None,
    ) -> None:
        """Initialize Ollama provider."""

        self._settings = settings if settings is not None else LLMSettings()

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """Generate response from Ollama."""

        payload = {
            "model": self._settings.model,
            "system": request.system_prompt,
            "prompt": request.user_prompt,
            "stream": False,
        }

        try:
            response = requests.post(
                f"{self._settings.base_url}/api/generate",
                json=payload,
                timeout=self._settings.timeout,
            )

        except requests.RequestException as exc:
            raise ProviderUnavailableError("Ollama server is unavailable.") from exc

        if response.status_code != 200:
            raise GenerationError(f"Ollama request failed: {response.text}")

        try:
            data = response.json()

        except ValueError as exc:
            raise GenerationError("Invalid JSON returned by Ollama.") from exc

        return LLMResponse(
            text=data.get(
                "response",
                "",
            ),
            model=data.get(
                "model",
                self._settings.model,
            ),
        )
