"""
Resolved citation model.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ResolvedCitation:
    """Citation enriched with explanation."""

    document_name: str

    page: int

    snippet: str

    score: float

    reasons: tuple[str, ...] = ()