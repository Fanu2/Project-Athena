"""
Evidence intelligence model.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class EvidenceRecord:
    """
    Authoritative evidence unit used by retrieval,
    citation, and document navigation.
    """

    document_id: str

    document_name: str

    document_path: Path

    chunk_id: str

    page: int

    text: str

    #
    # Retrieval ranking signals
    #

    semantic_score: float = 0.0

    keyword_score: float = 0.0

    metadata_score: float = 0.0

    identity_score: float = 0.0

    document_authority_score: float = 0.0

    #
    # Final ranking result
    #

    final_score: float = 0.0

    #
    # Human-readable explanation
    #

    ranking_reasons: tuple[str, ...] = ()

    #
    # A19 Retrieval Intelligence metadata
    #

    retrieval_strategy: str = "hybrid"

    ranking_profile: str = "default"

    planner_confidence: float = 0.0
