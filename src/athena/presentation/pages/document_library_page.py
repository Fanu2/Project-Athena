"""
Document library page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.documents.models import Document
from athena.documents.service import DocumentService
from athena.presentation.widgets.document_table import (
    DocumentTable,
)
from athena.presentation.widgets.document_toolbar import (
    DocumentToolbar,
)


class DocumentLibraryPage(QWidget):
    """Workspace document library."""

    def __init__(
        self,
        parent: QWidget |None = None,
    ) -> None:
        """Initialize the document library page."""

        super().__init__(parent)

        self._document_service: DocumentService | None = None

        self.toolbar = DocumentToolbar()
        self.table = DocumentTable()
        self.status_label = QLabel()

        self._setup_ui()

        self.clear_document_service()

    def _setup_ui(self) -> None:
        """Configure the page layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.table)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def set_document_service(
        self,
        service: DocumentService,
    ) -> None:
        """Attach a document service to the page."""

        self._document_service = service
        self.refresh()

    def clear_document_service(self) -> None:
        """Detach the current document service."""

        self._document_service = None

        self.table.clear()
        self.status_label.setText("No workspace open")

    @property
    def documents_directory(self) -> Path | None:
        """Return the active workspace documents directory."""

        if self._document_service is None:
            return None

        return self._document_service.documents_dir

    def refresh(self) -> None:
        """Reload documents from the active workspace."""

        if self._document_service is None:
            self.table.clear()
            self.status_label.setText("No workspace open")
            return

        documents = self._document_service.list_documents()

        self.table.set_documents(documents)

        self.status_label.setText(
            f"{len(documents)} document(s)"
        )

    def selected_document(self) -> Document | None:
        """Return the selected document."""

        return self.table.selected_document()

    def import_document(
        self,
        source: Path,
    ) -> None:
        """Import a document into the active workspace."""

        if self._document_service is None:
            return

        self._document_service.import_document(source)

        self.refresh()

    def delete_selected_document(self) -> None:
        """Delete the selected document."""

        if self._document_service is None:
            return

        document = self.selected_document()

        if document is None:
            return

        self._document_service.remove_document(
            document.path,
        )

        self.refresh()

    def clear(self) -> None:
        """Clear the document table."""

        self.table.clear()

        if self._document_service is None:
            self.status_label.setText("No workspace open")
        else:
            self.status_label.setText("0 document(s)")