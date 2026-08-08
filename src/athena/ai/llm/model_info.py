"""
Model information model.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena.ai.llm.capabilities import ModelCapabilities


@dataclass(frozen=True, slots=True)
class ModelInfo:
    """Describes an available LLM model."""

    name: str

    provider: str

    context_window: int = 0

    capabilities: ModelCapabilities = field(
        default_factory=ModelCapabilities
    )

    # Legacy compatibility fields.
    # Kept during A16 migration to avoid breaking existing contracts.
    supports_chat: bool = True

    supports_streaming: bool = False

    supports_tools: bool = False

    supports_vision: bool = False