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

    semantic_score: float = 0.0

    keyword_score: float = 0.0

    metadata_score: float = 0.0

    identity_score: float = 0.0

    document_authority_score: float = 0.0

    final_score: float = 0.0

    ranking_reasons: tuple[str, ...] = ()