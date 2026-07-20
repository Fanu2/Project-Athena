"""
LLM data models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LLMRequest:
    """
    Request sent to an LLM provider.
    """

    system_prompt: str

    user_prompt: str

    model_name: str = "gemma3:4b"


@dataclass(slots=True, frozen=True)
class LLMResponse:
    """
    Response returned by an LLM provider.
    """

    text: str

    model: str