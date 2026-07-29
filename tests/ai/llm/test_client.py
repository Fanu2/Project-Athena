"""
Tests for LLM client.
"""

from __future__ import annotations

import pytest

from athena.ai.llm import LLMClient
from athena.ai.llm import LLMRequest
from athena.ai.llm import LLMResponse
from athena.ai.llm import LLMProvider
from athena.ai.llm import ProviderRegistry


class FakeProvider(LLMProvider):
    """Fake provider for testing."""

    @property
    def provider_name(self) -> str:
        return "fake"

    def analyze(
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

    response = client.analyze(
        LLMRequest(
            system_prompt="System",
            user_prompt="Question",
        )
    )

    assert response.text == "Test response"
    assert response.model == "fake-model"



def test_client_accepts_registry() -> None:
    provider = FakeProvider()

    registry = ProviderRegistry()
    registry.register(provider)

    client = LLMClient(registry=registry)

    assert client.provider is provider
    assert client.registry is registry


def test_client_requires_provider_or_registry() -> None:
    with pytest.raises(ValueError):
        LLMClient()


def test_client_uses_default_provider_from_registry() -> None:
    provider = FakeProvider()

    registry = ProviderRegistry()
    registry.register(provider)

    client = LLMClient(registry=registry)

    response = client.analyze(
        LLMRequest(
            system_prompt="System",
            user_prompt="Hello",
        ),
    )

    assert response.text == "Test response"





