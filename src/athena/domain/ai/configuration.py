"""
AI generation configuration.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class AIConfiguration:
    """Configuration for a single AI request."""

    model: str
    temperature: float
    max_tokens: int
    top_k: int
