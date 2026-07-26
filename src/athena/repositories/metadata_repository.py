"""
Repository interface for document metadata.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from uuid import UUID

from athena.domain import DocumentMetadata


class MetadataRepository(ABC):
    """Abstract repository for document metadata."""

    @abstractmethod
    def add(
        self,
        metadata: DocumentMetadata,
    ) -> None:
        """Store metadata."""
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        document_id: UUID,
    ) -> DocumentMetadata | None:
        """Retrieve metadata for a document."""
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
    ) -> list[DocumentMetadata]:
        """Return all metadata records."""
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        metadata: DocumentMetadata,
    ) -> None:
        """Update metadata."""
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        document_id: UUID,
    ) -> None:
        """Delete metadata."""
        raise NotImplementedError
