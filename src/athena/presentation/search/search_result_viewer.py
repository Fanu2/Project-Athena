"""
Search result viewer.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from athena.indexing.models import DocumentChunk


class SearchResultViewer(QWidget):
    """Displays selected search result details."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.title_label = QLabel(
            "No result selected",
        )

        self.content = QTextEdit()

        self.content.setReadOnly(True)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Create layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.title_label,
        )

        layout.addWidget(
            self.content,
        )

    def show_chunk(
        self,
        chunk: DocumentChunk,
    ) -> None:
        """Display a document chunk."""

        self.title_label.setText(
            f"Document: {chunk.document_id} | Page: {chunk.page_number}",
        )

        self.content.setText(
            chunk.text,
        )

    def clear(self) -> None:
        """Clear viewer."""

        self.title_label.setText(
            "No result selected",
        )

        self.content.clear()
