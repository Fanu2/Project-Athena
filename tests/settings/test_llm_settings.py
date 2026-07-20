"""
Tests for LLM settings.
"""

from __future__ import annotations

from athena.settings import LLMSettings


def test_default_llm_settings() -> None:
    """Default settings are configured correctly."""

    settings = LLMSettings()

    assert settings.provider == "ollama"

    assert settings.model == "gemma3:4b"

    assert settings.base_url == (
        "http://localhost:11434"
    )

    assert settings.timeout == 120