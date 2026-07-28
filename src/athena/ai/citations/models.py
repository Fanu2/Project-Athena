"""
Project Athena

Citation domain models.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Citation:
    """Represents a citation to a retrieved document."""

    document_id: str

    title: str

    page_number: int

    start_offset: int

    end_offset: int

    score: float


@dataclass(slots=True)
class CitationReport:
    """Collection of citations."""

    citations: list[Citation] = field(default_factory=list)
