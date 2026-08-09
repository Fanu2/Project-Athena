"""
LLM configuration settings.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LLMSettings:
    """
    Configuration for LLM providers.
    """

    provider: str = "ollama"

    model: str = "qwen2.5:1.5b"

    base_url: str = (
        "http://localhost:11434"
    )

    timeout: int = 120

    api_key: str = ""