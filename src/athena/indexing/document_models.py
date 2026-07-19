"""
Document metadata models.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True, frozen=True)
class IndexedDocument:
    """Metadata describing an indexed document."""

    document_id: str
    path: Path
    title: str
    sha256: str
    page_count: int
    indexed_at: datetime
