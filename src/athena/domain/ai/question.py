"""
AI question model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Question:
    """Represents a user's question."""

    text: str
