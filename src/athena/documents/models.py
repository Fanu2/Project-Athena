"""
Document models.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(slots=True)
class Document:
    """
    Metadata describing a document stored in a workspace.
    """

    id: str
    name: str
    path: Path
    size: int
    created: datetime
    modified: datetime