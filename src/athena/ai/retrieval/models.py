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

    document_name: str = ""

    semantic_score: float = 0.0

    keyword_score: float = 0.0

    metadata_score: float = 0.0

    identity_score: float = 0.0

    document_authority_score: float = 0.0


