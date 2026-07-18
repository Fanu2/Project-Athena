"""
Bookmark models.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Bookmark:
    """A bookmarked document."""

    document_id: str

    created: datetime
