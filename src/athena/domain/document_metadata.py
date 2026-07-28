"""
Document metadata domain model.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(slots=True)
class DocumentMetadata:
    """
    AI-generated metadata associated with a document.

    This model intentionally stores metadata that is not part of the
    core Document entity.
    """

    document_id: UUID

    language: str | None = None

    page_count: int | None = None

    last_indexed: datetime | None = None

    metadata_version: int = 1

