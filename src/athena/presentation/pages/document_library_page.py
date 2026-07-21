"""
Document library page.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QLabel,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from athena.bookmarks.service import BookmarkService
from athena.documents.models import Document
from athena.notes.service import NoteService
from athena.presentation.widgets.document_details import (
    DocumentDetails,
)
from athena.presentation.widgets.document_table import (
    DocumentTable,
)
from athena.presentation.widgets.document_toolbar import (
    DocumentToolbar,
)
from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)


class DocumentLibraryPage(QWidget):
    """Workspace document library."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._document_service: WorkspaceDocumentService | None = None
        self._bookmark_service: BookmarkService | None = None
        self._note_service: NoteService | None = None

        self.toolbar = DocumentToolbar()
        self.table = DocumentTable()
        self.details = DocumentDetails()
        self.status_label = QLabel()

        self._setup_ui()

        self.table.table.itemSelectionChanged.connect(
            self._on_document_selected,
        )

        self.clear_document_service()

    def _setup_ui(self) -> None:
        """Configure the page layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(self.toolbar)

        splitter = QSplitter()

        splitter.addWidget(self.table)
        splitter.addWidget(self.details)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 1)

        layout.addWidget(splitter)
        layout.addWidget(self.status_label)

    def set_document_service(
        self,
        service: WorkspaceDocumentService,
    ) -> None:
        """Attach a document service to the page."""

        self._document_service = service
        self.refresh()

    @property
    def document_service(self) -> WorkspaceDocumentService | None:
        """Return the current document service."""

        return self._document_service

    def set_bookmark_service(
        self,
        service: BookmarkService,
    ) -> None:
        """Attach bookmark service."""

        self._bookmark_service = service
        self.details.set_bookmark_service(service)

    def set_note_service(
        self,
        service: NoteService,
    ) -> None:
        """Attach note service."""

        self._note_service = service
        self.details.set_note_service(service)

    def clear_document_service(self) -> None:
        """Detach the current document service."""

        self._document_service = None
        self._bookmark_service = None
        self._note_service = None

        self.table.clear()
        self.details.clear()

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
            self.details.clear()
            self.status_label.setText("No workspace open")
            return

        documents = self._document_service.list_documents()

        self.table.set_documents(documents)
        self.status_label.setText(f"{len(documents)} document(s)")

    def refresh_documents(self) -> None:
        """
        Public API used by background import workflows.

        This method is intended to be called after asynchronous
        document imports complete.
        """

        self.refresh()

    def _on_document_selected(self) -> None:
        """Display the selected document."""

        document = self.selected_document()

        if document is None:
            self.details.clear()
            return

        self.details.show_document(document)

    def selected_document(self) -> Document | None:
        """Return the selected document."""

        return self.table.selected_document()

    def import_document(
        self,
        source: Path,
    ) -> None:
        """Import a single document."""

        if self._document_service is None:
            return

        self._document_service.import_document(source)
        self.refresh()

    def import_folder(
        self,
        folder: Path,
    ) -> None:
        """Import all supported documents in a folder."""

        if self._document_service is None:
            return

        self._document_service.import_folder(folder)
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
        """Clear the page."""

        self.table.clear()
        self.details.clear()

        if self._document_service is None:
            self.status_label.setText("No workspace open")
        else:
            self.status_label.setText("0 document(s)")
