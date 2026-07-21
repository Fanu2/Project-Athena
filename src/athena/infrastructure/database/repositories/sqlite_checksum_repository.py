"""
Document repository interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from uuid import UUID

from athena.domain.document import Document


class DocumentRepository(ABC):
    """Repository interface for documents."""

    @abstractmethod
    def add(
        self,
        document: Document,
    ) -> None:
        """Persist a document."""

    @abstractmethod
    def get(
        self,
        document_id: UUID,
    ) -> Document | None:
        """Return a document."""

    @abstractmethod
    def get_all(
        self,
    ) -> list[Document]:
        """Return all documents."""

    @abstractmethod
    def update(
        self,
        document: Document,
    ) -> None:
        """Update a document."""

    @abstractmethod
    def delete(
        self,
        document_id: UUID,
    ) -> None:
        """Delete a document."""

    @abstractmethod
    def exists(
        self,
        file_path: str,
    ) -> bool:
        """Return True if the document already exists."""
