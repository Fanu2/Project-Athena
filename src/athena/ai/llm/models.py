"""
LLM models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LLMRequest:
    """Request sent to a language model."""

    prompt: str
    model_name: str
    temperature: float = 0.0


@dataclass(slots=True, frozen=True)
class LLMResponse:
    """Response returned by a language model."""

    text: str
    model_name: str
