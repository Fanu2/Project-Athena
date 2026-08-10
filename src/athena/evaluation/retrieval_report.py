"""
Project Athena

Module: retrieval_report

Retrieval Intelligence Report domain models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RetrievalCandidate:
    """
    A ranked retrieval candidate.

    Preserves retrieval evidence identity,
    source navigation metadata, and ranking signals.
    """

    document_id: str

    title: str

    final_score: float

    #
    # A19.4 Evidence identity metadata
    #

    document_name: str = ""

    chunk_id: str = ""

    page: int = 0

    #
    # Ranking signals
    #

    semantic_score: float = 0.0

    keyword_score: float = 0.0

    metadata_score: float = 0.0

    identity_score: float = 0.0

    document_authority_score: float = 0.0

    #
    # Explanation
    #

    explanation: str = ""


@dataclass(slots=True)
class RetrievalReport:
    """
    Report describing a retrieval operation.

    Contains ranked evidence candidates and
    retrieval intelligence metadata.
    """

    query: str

    strategy: str

    latency_ms: float

    candidate_count: int

    results: list[RetrievalCandidate] = field(
        default_factory=list,
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )
