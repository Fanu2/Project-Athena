"""
Citation presentation model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class CitationView:
    """UI-friendly citation representation."""

    document_name: str

    page: int

    snippet: str

    score: float

    ranking_reasons: tuple[str, ...] = ()
