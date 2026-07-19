"""
Document library service.
"""

from __future__ import annotations

from athena.indexing.models import IndexedDocument
from athena.indexing.repositories.document_base import DocumentRepository


class DocumentLibraryService:
    """Application service for browsing indexed documents."""

    def __init__(
        self,
        repository: DocumentRepository,
    ) -> None:
        self._repository = repository

    def list_documents(
        self,
    ) -> list[IndexedDocument]:
        """Return all indexed documents."""

        return self._repository.list_documents()

    def search_by_title(
        self,
        title: str,
    ) -> list[IndexedDocument]:
        """Search indexed documents by title."""

        return self._repository.find_by_title(
            title,
        )
