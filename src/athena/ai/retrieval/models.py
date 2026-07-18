"""
Retrieval models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class SemanticResult:
    """Semantic search result."""

    chunk_id: str
    document_id: str
    page_number: int
    text: str
    score: float
