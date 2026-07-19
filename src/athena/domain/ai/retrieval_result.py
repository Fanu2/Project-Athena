"""
Retrieval result model.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class RetrievalResult:
    """One retrieved document passage."""

    document_id: UUID
    document_name: str
    page: int
    text: str
    score: float
