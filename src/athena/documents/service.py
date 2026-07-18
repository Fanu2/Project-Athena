"""
Document service.
"""

from __future__ import annotations

from pathlib import Path

from athena.documents.models import Document
from athena.documents.storage import DocumentStorage
from athena.documents.validators import validate_document


class DocumentService:
    """High-level document management service."""

    def __init__(
        self,
        documents_dir: Path,
    ) -> None:
        """
        Initialize the document service.

        Args:
            documents_dir:
                Directory where workspace documents are stored.
        """

        self._documents_dir = documents_dir

    @property
    def documents_dir(self) -> Path:
        """Return the workspace documents directory."""

        return self._documents_dir

    def import_document(
        self,
        source: Path,
    ) -> Path:
        """
        Validate and import a document into the workspace.

        Args:
            source:
                Source document path.

        Returns:
            Destination path inside the workspace.
        """

        validate_document(source)

        return DocumentStorage.copy_document(
            source,
            self._documents_dir,
        )

    def remove_document(
        self,
        document: Path,
    ) -> None:
        """
        Remove a document from the workspace.
        """

        DocumentStorage.remove_document(document)

    def list_documents(self) -> list[Document]:
        """
        Return all documents in the workspace.
        """

        return DocumentStorage.list_documents(
            self._documents_dir,
        )