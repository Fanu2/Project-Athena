"""
SQLite implementation of the MetadataRepository interface.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from athena.domain.document_metadata import DocumentMetadata
from athena.infrastructure.database.models.document_metadata_model import (
    DocumentMetadataModel,
)
from athena.repositories.metadata_repository import MetadataRepository


class SqliteMetadataRepository(MetadataRepository):
    """SQLite implementation of MetadataRepository."""

    def __init__(self, session: Session):
        self._session = session

    def add(self, metadata: DocumentMetadata) -> None:
        model = DocumentMetadataModel(
            document_id=str(metadata.document_id),
            language=metadata.language,
            page_count=metadata.page_count,
            last_indexed=metadata.last_indexed,
            metadata_version=metadata.metadata_version,
        )
        self._session.add(model)
        self._session.commit()

    def get(self, document_id: UUID) -> DocumentMetadata | None:
        model = self._session.get(
            DocumentMetadataModel,
            str(document_id),
        )

        if model is None:
            return None

        return DocumentMetadata(
            document_id=UUID(model.document_id),
            language=model.language,
            page_count=model.page_count,
            last_indexed=model.last_indexed,
            metadata_version=model.metadata_version,
        )

    def get_all(self) -> list[DocumentMetadata]:
        models = self._session.query(DocumentMetadataModel).all()

        return [
            DocumentMetadata(
                document_id=UUID(model.document_id),
                language=model.language,
                page_count=model.page_count,
                last_indexed=model.last_indexed,
                metadata_version=model.metadata_version,
            )
            for model in models
        ]

    def update(self, metadata: DocumentMetadata) -> None:
        model = self._session.get(
            DocumentMetadataModel,
            str(metadata.document_id),
        )

        if model is None:
            raise ValueError("Metadata not found.")

        model.language = metadata.language
        model.page_count = metadata.page_count
        model.last_indexed = metadata.last_indexed
        model.metadata_version = metadata.metadata_version

        self._session.commit()

    def delete(self, document_id: UUID) -> None:
        model = self._session.get(
            DocumentMetadataModel,
            str(document_id),
        )

        if model is not None:
            self._session.delete(model)
            self._session.commit()

