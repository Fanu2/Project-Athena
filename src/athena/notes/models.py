"""
Note models.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class Note:
    """A research note attached to a document."""

    document_id: str
    content: str
    created: datetime
    modified: datetime
