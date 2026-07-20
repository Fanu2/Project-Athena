"""
Citation models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Citation:
    """Represents a citation to a document passage."""

    document_id: str

    title: str

    page_number: int

    start_offset: int

    end_offset: int

    score: float