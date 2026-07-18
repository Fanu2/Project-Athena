"""
Document actions.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from athena.presentation.pages.document_library_page import (
    DocumentLibraryPage,
)


class DocumentActions:
    """Controller for document library actions."""

    def __init__(
        self,
        page: DocumentLibraryPage,
    ) -> None:
        """Initialize the document actions."""

        self._page = page

        self._connect_signals()

    def _connect_signals(self) -> None:
        """Connect toolbar signals."""

        self._page.toolbar.import_button.clicked.connect(self.import_document)

        self._page.toolbar.delete_button.clicked.connect(self.delete_document)

        self._page.toolbar.refresh_button.clicked.connect(self._page.refresh)

        self._page.toolbar.open_folder_button.clicked.connect(self.open_documents_folder)

    def import_document(self) -> None:
        """Import a document."""

        filename, _ = QFileDialog.getOpenFileName(
            self._page,
            "Import Document",
            "",
            ("Documents (*.pdf *.txt *.md);;" "All Files (*)"),
        )

        if not filename:
            return

        try:
            self._page.import_document(
                Path(filename),
            )

        except Exception as exc:
            QMessageBox.critical(
                self._page,
                "Import Failed",
                str(exc),
            )

    def delete_document(self) -> None:
        """Delete the selected document."""

        document = self._page.selected_document()

        if document is None:
            QMessageBox.information(
                self._page,
                "Delete Document",
                "Please select a document.",
            )
            return

        answer = QMessageBox.question(
            self._page,
            "Delete Document",
            (f"Delete '{document.name}'?"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if answer != QMessageBox.Yes:
            return

        self._page.delete_selected_document()

    def open_documents_folder(self) -> None:
        """Open the workspace documents folder."""

        folder = self._page._document_service._documents_dir

        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder)))
