"""
Citation model.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class Citation:
    """Evidence supporting an AI answer."""

    document_id: UUID
    document_name: str
    page: int
    snippet: str
    score: float
