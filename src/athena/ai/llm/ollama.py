"""
Ollama LLM provider.
"""

from __future__ import annotations

from typing import Any

import requests

from athena.ai.llm.models import (
    LLMRequest,
    LLMResponse,
)
from athena.ai.llm.provider import (
    LLMProvider,
)


class OllamaProvider(LLMProvider):
    """Ollama local model provider."""

    def __init__(
        self,
        endpoint: str = "http://localhost:11434/api/generate",
    ) -> None:
        """Initialize Ollama provider."""

        self._endpoint = endpoint

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """Generate response from Ollama."""

        payload: dict[str, Any] = {
            "model": request.model_name,
            "prompt": request.prompt,
            "temperature": request.temperature,
            "stream": False,
        }

        response = requests.post(
            self._endpoint,
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data: dict[str, Any] = response.json()

        text = data.get(
            "response",
            "",
        )

        if not isinstance(
            text,
            str,
        ):
            text = str(text)

        return LLMResponse(
            text=text,
            model_name=request.model_name,
        )
