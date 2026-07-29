"""
Tests for OpenAIProvider.
"""

from __future__ import annotations

import pytest

from athena.ai.llm.providers import OpenAIProvider
from athena.settings import LLMSettings


def test_provider_name() -> None:
    provider = OpenAIProvider()

    assert provider.provider_name == "openai"


def test_default_settings() -> None:
    provider = OpenAIProvider()

    assert provider._settings.provider == "openai"
    assert provider._settings.model == "gpt-5"
    assert provider._settings.base_url == "https://api.openai.com"


def test_custom_settings() -> None:
    settings = LLMSettings(
        provider="openai",
        model="custom-model",
        base_url="https://example.com",
        api_key="test-key",
    )

    provider = OpenAIProvider(settings)

    assert provider._settings == settings


def test_missing_api_key_validation() -> None:
    provider = OpenAIProvider()

    with pytest.raises(ValueError):
        provider.validate_configuration()


def test_valid_configuration() -> None:
    provider = OpenAIProvider(
        LLMSettings(
            provider="openai",
            model="gpt-5",
            base_url="https://api.openai.com",
            api_key="test-key",
        )
    )

    provider.validate_configuration()
