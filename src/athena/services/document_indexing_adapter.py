"""
Bridge between workspace documents and Athena document library.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4

from athena.domain import Document
from athena.infrastructure.database.repositories.sqlite_document_repository import (
    SqliteDocumentRepository,
)


class DocumentIndexingAdapter:
    """Register workspace documents in Athena library."""

    def __init__(
        self,
        repository: SqliteDocumentRepository,
    ) -> None:
        self._repository = repository

    def register(
        self,
        document_path: Path,
    ) -> Document:
        """Register a document if not already present."""

        existing = self._repository.get_by_path(
            str(document_path),
        )

        if existing is not None:
            return existing

        document = Document(
            id=uuid4(),
            filename=document_path.name,
            title=document_path.stem,
            file_path=document_path,
            file_type=document_path.suffix.lower(),
            file_size=document_path.stat().st_size,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        self._repository.add(
            document,
        )

        return document
