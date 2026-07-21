"""
Retrieval models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class SemanticResult:
    """Semantic search result."""

    chunk_id: str

    document_id: str

    document_title: str

    page_number: int

    start_offset: int

    end_offset: int

    text: str

    score: float
