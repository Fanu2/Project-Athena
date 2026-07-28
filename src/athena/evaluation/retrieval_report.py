"""
Project Athena
Module: retrieval_report

Retrieval Intelligence Report domain models.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RetrievalCandidate:
    """A ranked retrieval candidate."""

    document_id: str
    title: str

    final_score: float

    semantic_score: float = 0.0
    keyword_score: float = 0.0
    metadata_score: float = 0.0
    identity_score: float = 0.0

    explanation: str = ""


@dataclass(slots=True)
class RetrievalReport:
    """Report describing a retrieval operation."""

    query: str
    strategy: str

    latency_ms: float
    candidate_count: int

    results: list[RetrievalCandidate] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
