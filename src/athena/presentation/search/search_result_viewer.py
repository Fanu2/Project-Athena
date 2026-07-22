"""
Search result viewer.
"""

from __future__ import annotations

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from athena.documents.service import DocumentService
from athena.indexing.models import DocumentChunk


class SearchResultViewer(QWidget):
    """Displays selected search result details."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._current_chunk: DocumentChunk | None = None

        self._document_service: DocumentService | None = None

        self.title_label = QLabel(
            "No result selected",
        )

        self.content = QTextEdit()

        self.content.setReadOnly(True)

        self.open_button = QPushButton(
            "Open Document",
        )

        self.open_button.setEnabled(False)

        self._setup_ui()

        self.open_button.clicked.connect(
            self._open_document,
        )

    def _setup_ui(self) -> None:
        """Create layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.title_label,
        )

        layout.addWidget(
            self.content,
        )

        layout.addWidget(
            self.open_button,
        )

    def set_document_service(
        self,
        service: DocumentService,
    ) -> None:
        """Set document service."""

        self._document_service = service

    def clear_document_service(self) -> None:
        """Clear document service."""

        self._document_service = None

        self.clear()

    def show_chunk(
        self,
        chunk: DocumentChunk,
    ) -> None:
        """Display a document chunk."""

        self._current_chunk = chunk

        self.title_label.setText(
            f"Document: {chunk.document_id} | Page: {chunk.page_number}",
        )

        self.content.setText(
            chunk.text,
        )

        self.open_button.setEnabled(
            self._document_service is not None,
        )

    def _open_document(self) -> None:
        """Open the source document."""

        if self._current_chunk is None:
            return

        if self._document_service is None:
            return

        document = self._document_service.get_document(
            self._current_chunk.document_id,
        )

        if document is None:
            return

        QDesktopServices.openUrl(
            QUrl.fromLocalFile(
                str(document.path),
            ),
        )

    def clear(self) -> None:
        """Clear viewer."""

        self._current_chunk = None

        self.title_label.setText(
            "No result selected",
        )

        self.content.clear()

        self.open_button.setEnabled(
            False,
        )
