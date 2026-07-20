"""
Document actions.
"""

from __future__ import annotations

import traceback
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from athena.presentation.importing import ImportManager
from athena.presentation.pages.document_library_page import (
    DocumentLibraryPage,
)


class DocumentActions:
    """Controller for document library actions."""

    def __init__(
        self,
        page: DocumentLibraryPage,
    ) -> None:
        """Initialize document actions."""

        self._page = page
        self._import_manager = ImportManager()

        self._connect_signals()

    def _connect_signals(self) -> None:
        """Connect toolbar actions."""

        toolbar = self._page.toolbar

        toolbar.import_button.clicked.connect(
            self.import_document,
        )

        toolbar.import_folder_button.clicked.connect(
            self.import_folder,
        )

        toolbar.delete_button.clicked.connect(
            self.delete_document,
        )

        toolbar.refresh_button.clicked.connect(
            self._page.refresh_documents,
        )

        toolbar.open_folder_button.clicked.connect(
            self.open_documents_folder,
        )

    def import_document(self) -> None:
        """Import a single document."""

        service = self._page.document_service

        if service is None:
            QMessageBox.information(
                self._page,
                "No Workspace",
                "Open a workspace first.",
            )
            return

        filename, _ = QFileDialog.getOpenFileName(
            self._page,
            "Import Document",
            "",
            (
                "Documents "
                "(*.pdf *.docx *.txt *.md);;"
                "All Files (*)"
            ),
        )

        if not filename:
            return

        try:
            self._import_manager.import_documents(
                parent=self._page,
                document_service=service,
                page=self._page,
                documents=[
                    Path(filename),
                ],
            )

        except Exception as exc:
            traceback.print_exc()

            QMessageBox.critical(
                self._page,
                "Import Failed",
                f"{type(exc).__name__}\n\n{exc}",
            )

    def import_folder(self) -> None:
        """Import all supported documents from a folder."""

        service = self._page.document_service

        if service is None:
            QMessageBox.information(
                self._page,
                "No Workspace",
                "Open a workspace first.",
            )
            return

        folder = QFileDialog.getExistingDirectory(
            self._page,
            "Import Folder",
        )

        if not folder:
            return

        documents: list[Path] = []

        for pattern in (
            "*.pdf",
            "*.docx",
            "*.txt",
            "*.md",
        ):
            documents.extend(
                Path(folder).glob(pattern),
            )

        if not documents:
            QMessageBox.information(
                self._page,
                "Import Folder",
                "No supported documents were found.",
            )
            return

        try:
            self._import_manager.import_documents(
                parent=self._page,
                document_service=service,
                page=self._page,
                documents=documents,
            )

        except Exception as exc:
            traceback.print_exc()

            QMessageBox.critical(
                self._page,
                "Import Folder Failed",
                f"{type(exc).__name__}\n\n{exc}",
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
            f"Delete '{document.name}'?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self._page.delete_selected_document()

    def open_documents_folder(self) -> None:
        """Open the workspace documents folder."""

        folder = self._page.documents_directory

        if folder is None:
            QMessageBox.information(
                self._page,
                "No Workspace",
                "Open a workspace first.",
            )
            return

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(folder),
            ),
        )