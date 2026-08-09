"""
Tests for LLM settings.
"""

from __future__ import annotations

from athena.settings import LLMSettings


def test_default_llm_settings() -> None:
    """Default settings use the resource-friendly local AI configuration."""

    settings = LLMSettings()

    assert settings.provider == "ollama"

    assert settings.model == "qwen2.5:1.5b"

    assert settings.base_url == (
        "http://localhost:11434"
    )

    assert settings.timeout == 120
