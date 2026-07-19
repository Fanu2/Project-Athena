"""
Document repository interface.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from athena.indexing.models import IndexedDocument


class DocumentRepository(ABC):
    """Abstract repository for indexed document metadata."""

    @abstractmethod
    def save_document(
        self,
        document: IndexedDocument,
    ) -> None:
        """Save document metadata."""

    @abstractmethod
    def load_document(
        self,
        document_id: str,
    ) -> IndexedDocument | None:
        """Load a document by its ID."""

    @abstractmethod
    def exists_by_hash(
        self,
        sha256: str,
    ) -> bool:
        """Return True if a document with the given SHA-256 exists."""

    @abstractmethod
    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """Delete document metadata."""
