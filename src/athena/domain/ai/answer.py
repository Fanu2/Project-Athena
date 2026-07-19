"""
AI answer model.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from athena.domain.ai.citation import Citation


@dataclass(slots=True)
class Answer:
    """AI-generated answer."""

    text: str

    citations: list[Citation] = field(default_factory=list)
