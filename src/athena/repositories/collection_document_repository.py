"""
Collection document repository interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from uuid import UUID


class CollectionDocumentRepository(ABC):
    """
    Repository interface for collection-document links.
    """

    @abstractmethod
    def add_document(
        self,
        collection_id: UUID,
        document_id: str,
    ) -> None:
        """Add document to collection."""

        raise NotImplementedError

    @abstractmethod
    def remove_document(
        self,
        collection_id: UUID,
        document_id: str,
    ) -> None:
        """Remove document from collection."""

        raise NotImplementedError

    @abstractmethod
    def get_documents(
        self,
        collection_id: UUID,
    ) -> list[str]:
        """Return documents in collection."""

        raise NotImplementedError

    @abstractmethod
    def get_collections(
        self,
        document_id: str,
    ) -> list[UUID]:
        """Return collections containing document."""

        raise NotImplementedError