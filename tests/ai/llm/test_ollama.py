"""
Tests for Ollama provider.
"""

from __future__ import annotations

from unittest.mock import Mock
from unittest.mock import patch

from athena.ai.llm.models import LLMRequest
from athena.ai.llm.providers import OllamaProvider
from athena.settings import LLMSettings


def test_ollama_provider_generates_response() -> None:
    """Ollama provider parses response correctly."""

    provider = OllamaProvider(
        LLMSettings(
            model="gemma3:4b",
        ),
    )

    fake_response = Mock()

    fake_response.status_code = 200

    fake_response.json.return_value = {
        "response": "Hello from Athena",
        "model": "gemma3:4b",
    }

    with patch(
        "athena.ai.llm.providers.ollama.requests.post",
        return_value=fake_response,
    ):

        result = provider.generate(
            LLMRequest(
                system_prompt="You are Athena.",
                user_prompt="Hello",
            )
        )

    assert result.text == "Hello from Athena"

    assert result.model == "gemma3:4b"
