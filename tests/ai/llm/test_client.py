"""
Tests for LLM client.
"""

from __future__ import annotations

from athena.ai.llm import LLMClient
from athena.ai.llm import LLMRequest
from athena.ai.llm import LLMResponse
from athena.ai.llm import LLMProvider


class FakeProvider(LLMProvider):
    """Fake provider for testing."""

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        return LLMResponse(
            text="Test response",
            model="fake-model",
        )


def test_client_generates_response() -> None:
    """Client delegates generation to provider."""

    client = LLMClient(
        FakeProvider(),
    )

    response = client.generate(
        LLMRequest(
            system_prompt="System",
            user_prompt="Question",
        )
    )

    assert response.text == "Test response"
    assert response.model == "fake-model"
