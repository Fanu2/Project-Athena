"""
Model information model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ModelInfo:
    """Describes an available LLM model."""

    name: str

    provider: str

    context_window: int = 0

    supports_chat: bool = True

    supports_streaming: bool = False

    supports_tools: bool = False

    supports_vision: bool = False
