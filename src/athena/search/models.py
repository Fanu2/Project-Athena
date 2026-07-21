"""
Unified search models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SearchResult:
    """Represents a search result returned by the search service."""

    chunk_id: str

    document_id: str

    document_title: str

    page_number: int

    text: str

    score: float | None = None