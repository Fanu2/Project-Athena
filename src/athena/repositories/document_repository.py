"""
Document repository interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from uuid import UUID

from athena.domain import Document


class DocumentRepository(ABC):
    """Repository interface for documents."""

    @abstractmethod
    def get(
        self,
        document_id: UUID,
    ) -> Document | None:
        """Get document by ID."""

        raise NotImplementedError

    @abstractmethod
    def add(
        self,
        document: Document,
    ) -> None:
        """Add document."""

        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
    ) -> list[Document]:
        """Return all documents."""

        raise NotImplementedError

    @abstractmethod
    def exists(
        self,
        file_path: str,
    ) -> bool:
        """Check document existence."""

        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        document: Document,
    ) -> None:
        """Update document."""

        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        document_id: UUID,
    ) -> None:
        """Delete document."""

        raise NotImplementedError
