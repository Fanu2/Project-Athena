"""
Runtime request model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeRequest:
    """Describes an LLM execution request."""

    capability: str = "chat"

    preferred_model: str | None = None

    allow_fallback: bool = True
