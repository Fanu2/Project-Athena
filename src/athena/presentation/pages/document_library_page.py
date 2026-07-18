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
        document_service: DocumentService,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the document library page."""

        super().__init__(parent)

        self._document_service = document_service

        self.toolbar = DocumentToolbar()
        self.table = DocumentTable()
        self.status_label = QLabel()

        self._setup_ui()

        self.refresh()

    def _setup_ui(self) -> None:
        """Configure the page layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.table)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def refresh(self) -> None:
        """Reload documents from the workspace."""

        documents = self._document_service.list_documents()

        self.table.set_documents(documents)

        self.status_label.setText(f"{len(documents)} document(s)")

    def selected_document(self) -> Document | None:
        """Return the selected document."""

        return self.table.selected_document()

    def import_document(
        self,
        source: Path,
    ) -> None:
        """Import a document into the workspace."""

        self._document_service.import_document(
            source,
        )

        self.refresh()

    def delete_selected_document(self) -> None:
        """Delete the selected document."""

        document = self.selected_document()

        if document is None:
            return

        self._document_service.remove_document(
            document.path,
        )

        self.refresh()

    def clear(self) -> None:
        """Clear the page."""

        self.table.clear()

        self.status_label.setText("0 document(s)")
