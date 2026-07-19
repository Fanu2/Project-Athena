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

from athena.presentation.documents.document_table_model import (
    DocumentTableModel,
)


class DocumentBrowserWidget(QWidget):
    """Widget for browsing indexed documents."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

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

        top.addWidget(
            self._search,
        )

        layout = QVBoxLayout(self)

        layout.addLayout(
            top,
        )

        layout.addWidget(
            self._table,
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
