"""
Workspace document service.

Coordinates document management and indexing.
"""

from __future__ import annotations

from pathlib import Path

from athena.documents.models import Document
from athena.documents.service import DocumentService
from athena.indexing.service import IndexingService


class WorkspaceDocumentService:
    """High-level document workflow."""

    def __init__(
        self,
        document_service: DocumentService,
        indexing_service: IndexingService,
    ) -> None:
        """Initialize the service."""

        self._documents = document_service
        self._indexing = indexing_service

    @property
    def documents_dir(self) -> Path:
        """Return the workspace documents directory."""

        return self._documents.documents_dir

    def list_documents(self) -> list[Document]:
        """Return all documents."""

        return self._documents.list_documents()

    def import_document(
        self,
        source: Path,
    ) -> Path:
        """Import a document and index it."""

        document_path = self._documents.import_document(
            source,
        )

        self._indexing.index_document(
            document_path,
        )

        return document_path

    def remove_document(
        self,
        document_path: Path,
    ) -> None:
        """Remove a document."""

        self._documents.remove_document(
            document_path,
        )
