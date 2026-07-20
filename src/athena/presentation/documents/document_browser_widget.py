"""
Document browser widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QHeaderView,
    QLineEdit,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from athena.indexing.services.indexed_document_service import (
    IndexedDocumentService,
)
from athena.presentation.documents.document_table_model import (
    DocumentTableModel,
)


class DocumentBrowserWidget(QWidget):
    """Widget for browsing indexed documents."""

    def __init__(
        self,
        service: IndexedDocumentService | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._service = service

        self._search = QLineEdit()
        self._search.setPlaceholderText(
            "Search documents...",
        )

        self._table = QTableView()

        self._model = DocumentTableModel()

        self._table.setModel(
            self._model,
        )

        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch,
        )

        top = QHBoxLayout()
        top.addWidget(self._search)

        layout = QVBoxLayout(self)
        layout.addLayout(top)
        layout.addWidget(self._table)

        self._search.textChanged.connect(
            self._on_search_changed,
        )

        self.refresh()

    def set_document_service(
        self,
        service: IndexedDocumentService,
    ) -> None:
        """Attach or replace the document service."""

        self._service = service

        # Refresh after workspace/service becomes available.
        self.refresh()

    def refresh(
        self,
    ) -> None:
        """Reload indexed documents."""

        self._refresh()

    def _refresh(self) -> None:
        """Load all indexed documents."""

        if self._service is None:
            self._model.set_documents([])
            return

        documents = self._service.list_documents()

        self._model.set_documents(
            documents,
        )

    def _on_search_changed(
        self,
        text: str,
    ) -> None:
        """Filter documents by title."""

        if self._service is None:
            return

        text = text.strip()

        if text:
            documents = self._service.search_by_title(
                text,
            )
        else:
            documents = self._service.list_documents()

        self._model.set_documents(
            documents,
        )

    @property
    def model(
        self,
    ) -> DocumentTableModel:
        return self._model

    @property
    def table(
        self,
    ) -> QTableView:
        return self._table

    @property
    def search_box(
        self,
    ) -> QLineEdit:
        return self._search