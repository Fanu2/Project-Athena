"""
Document version domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class DocumentVersion:
    """Represents a version of an imported document."""

    id: UUID

    document_id: UUID

    version: int

    checksum: str

    size: int

    created_at: datetime