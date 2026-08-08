"""
AI provider domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Provider:
    """
    Represents an AI runtime provider.

    Examples:
    - Ollama
    - llama.cpp
    - OpenAI-compatible API
    """

    provider_id: str

    name: str

    endpoint: str | None = None

    models: list[str] = field(
        default_factory=list,
    )

    capabilities: set[str] = field(
        default_factory=set,
    )

    enabled: bool = True