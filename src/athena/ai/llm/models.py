"""
LLM data models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LLMRequest:
    """Request sent to an LLM."""

    system_prompt: str

    user_prompt: str


@dataclass(slots=True, frozen=True)
class LLMResponse:
    """Response returned by an LLM."""

    text: str

    model: str