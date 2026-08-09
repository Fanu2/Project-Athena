"""
Retrieval result model.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import UUID


@dataclass(slots=True, frozen=True)
class RetrievalResult:
    """
    One retrieved document passage.

    Carries retrieval scoring information,
    source navigation metadata, and retrieval
    intelligence context.
    """

    document_id: UUID

    document_name: str

    page: int

    text: str

    score: float

    document_path: Path | None = None

    #
    # Ranking signals
    #

    semantic_score: float = 0.0

    keyword_score: float = 0.0

    metadata_score: float = 0.0

    identity_score: float = 0.0

    document_authority_score: float = 0.0

    #
    # A19 Retrieval Intelligence metadata
    #

    retrieval_strategy: str = "hybrid"

    ranking_profile: str = "default"

    planner_confidence: float = 0.0
