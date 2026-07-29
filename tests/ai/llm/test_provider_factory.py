"""
Tests for ProviderFactory.
"""

from __future__ import annotations

import pytest

from athena.ai.llm import ProviderFactory
from athena.ai.llm.providers import (
    LMStudioProvider,
    OllamaProvider,
)
from athena.settings import LLMSettings


def test_create_ollama_provider() -> None:
    factory = ProviderFactory()

    provider = factory.create("ollama")

    assert isinstance(provider, OllamaProvider)


def test_create_lmstudio_provider() -> None:
    factory = ProviderFactory()

    provider = factory.create("lmstudio")

    assert isinstance(provider, LMStudioProvider)


def test_create_from_settings() -> None:
    settings = LLMSettings(provider="ollama")

    factory = ProviderFactory()

    provider = factory.create(settings=settings)

    assert isinstance(provider, OllamaProvider)


def test_default_settings_provider() -> None:
    factory = ProviderFactory()

    provider = factory.create()

    assert isinstance(provider, OllamaProvider)


def test_unknown_provider() -> None:
    factory = ProviderFactory()

    with pytest.raises(ValueError):
        factory.create("unknown")


def test_supported_providers() -> None:
    factory = ProviderFactory()

    assert factory.supported_providers() == [
        "ollama",
        "lmstudio",
    ]
