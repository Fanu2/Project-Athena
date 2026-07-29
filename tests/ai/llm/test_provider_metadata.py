"""
Tests for provider metadata.
"""

from __future__ import annotations

from athena.ai.llm.providers import (
    LMStudioProvider,
    OpenAIProvider,
    OllamaProvider,
)


def test_ollama_metadata() -> None:
    metadata = OllamaProvider().metadata

    assert metadata.name == "ollama"
    assert metadata.local is True
    assert metadata.requires_api_key is False


def test_lmstudio_metadata() -> None:
    metadata = LMStudioProvider().metadata

    assert metadata.name == "lmstudio"
    assert metadata.local is True
    assert metadata.requires_api_key is False


def test_openai_metadata() -> None:
    metadata = OpenAIProvider().metadata

    assert metadata.name == "openai"
    assert metadata.local is False
    assert metadata.requires_api_key is True
    assert metadata.supports_tools is True
    assert metadata.supports_vision is True
