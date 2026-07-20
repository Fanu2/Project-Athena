"""
Document domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import UUID


@dataclass(slots=True)
class Document:
    """Represents an imported document."""

    id: UUID

    filename: str

    title: str

    file_path: Path

    file_type: str

    file_size: int

    created_at: datetime

    updated_at: datetime