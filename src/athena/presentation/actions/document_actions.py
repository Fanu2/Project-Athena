"""
Document actions.
"""

from __future__ import annotations

import traceback
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QMessageBox,
)

from athena.knowledge.acquisition.providers.calibre_library import (
    CalibreLibraryReader,
)

from athena.presentation.dialogs.calibre_dialog import (
    CalibreDialog,
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

        toolbar.import_calibre_button.clicked.connect(
            self.import_calibre,
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

    def _require_workspace(self) -> bool:
        """
        Check that a workspace is available.
        """

        if self._page.document_service is None:
            QMessageBox.information(
                self._page,
                "No Workspace",
                "Open a workspace first.",
            )

            return False

        return True

    def _import_documents(
        self,
        documents: list[Path],
        error_title: str,
    ) -> None:
        """
        Send documents through the existing
        Athena import pipeline.
        """

        try:
            self._import_manager.import_documents(
                parent=self._page,
                document_service=self._page.document_service,
                page=self._page,
                documents=documents,
            )

        except Exception as exc:
            traceback.print_exc()

            QMessageBox.critical(
                self._page,
                error_title,
                f"{type(exc).__name__}\n\n{exc}",
            )

    def import_document(self) -> None:
        """Import a single document."""

        if not self._require_workspace():
            return

        filename, _ = QFileDialog.getOpenFileName(
            self._page,
            "Import Document",
            "",
            (
                "Documents "
                "(*.pdf *.docx *.txt *.md *.epub);;"
                "All Files (*)"
            ),
        )

        if not filename:
            return

        self._import_documents(
            [
                Path(filename),
            ],
            "Import Failed",
        )

    def import_folder(self) -> None:
        """Import supported documents from a folder."""

        if not self._require_workspace():
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
            "*.epub",
            "*.html",
            "*.htm",
            "*.odt",
            "*.xlsx",
        ):
            documents.extend(
                Path(folder).rglob(pattern),
            )

        if not documents:
            QMessageBox.information(
                self._page,
                "Import Folder",
                "No supported documents were found.",
            )

            return

        self._import_documents(
            documents,
            "Import Folder Failed",
        )

    def import_calibre(self) -> None:
        """
        Import books from a Calibre library.
        """

        if not self._require_workspace():
            return

        dialog = CalibreDialog(
            self._page,
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        library_path = dialog.library_path

        if library_path is None:
            return

        book_ids = dialog.selected_book_ids()

        if not book_ids:
            QMessageBox.information(
                self._page,
                "Calibre Import",
                "No books selected.",
            )

            return

        reader = CalibreLibraryReader(
            library_path,
        )

        documents: list[Path] = []

        for book_id in book_ids:
            try:
                documents.append(
                    reader.get_book_file(
                        book_id,
                        "EPUB",
                    )
                )

            except Exception as exc:
                QMessageBox.warning(
                    self._page,
                    "Book Skipped",
                    str(exc),
                )

        if not documents:
            QMessageBox.information(
                self._page,
                "Calibre Import",
                "No supported book files found.",
            )

            return

        self._import_documents(
            documents,
            "Calibre Import Failed",
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