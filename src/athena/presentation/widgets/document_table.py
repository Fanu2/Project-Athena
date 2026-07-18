"""
Document table widget.
"""

from __future__ import annotations


from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from athena.documents.models import Document


class DocumentTable(QWidget):
    """Table widget for displaying workspace documents."""

    COLUMN_NAME = 0
    COLUMN_SIZE = 1
    COLUMN_MODIFIED = 2

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize the document table."""

        super().__init__(parent)

        self._table = QTableWidget(self)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configure the user interface."""

        self._table.setColumnCount(3)

        self._table.setHorizontalHeaderLabels(
            [
                "Name",
                "Size (KB)",
                "Modified",
            ]
        )

        header = self._table.horizontalHeader()

        header.setSectionResizeMode(
            self.COLUMN_NAME,
            QHeaderView.Stretch,
        )

        header.setSectionResizeMode(
            self.COLUMN_SIZE,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            self.COLUMN_MODIFIED,
            QHeaderView.ResizeToContents,
        )

        self._table.setSelectionBehavior(QTableWidget.SelectRows)

        self._table.setSelectionMode(QTableWidget.SingleSelection)

        self._table.setEditTriggers(QTableWidget.NoEditTriggers)

        self._table.setAlternatingRowColors(True)

        self._table.setSortingEnabled(True)

        self._table.verticalHeader().setVisible(False)

        layout = QVBoxLayout(self)
        layout.addWidget(self._table)

        self.setLayout(layout)

    def set_documents(
        self,
        documents: list[Document],
    ) -> None:
        """Populate the table with documents."""

        self._table.setSortingEnabled(False)

        self._table.clearContents()
        self._table.setRowCount(len(documents))

        for row, document in enumerate(documents):

            name_item = QTableWidgetItem(
                document.name,
            )

            name_item.setData(
                Qt.ItemDataRole.UserRole,
                document,
            )

            size_kb = max(
                1,
                round(document.size / 1024),
            )

            size_item = QTableWidgetItem(
                str(size_kb),
            )

            modified_item = QTableWidgetItem(document.modified.strftime("%Y-%m-%d %H:%M"))

            self._table.setItem(
                row,
                self.COLUMN_NAME,
                name_item,
            )

            self._table.setItem(
                row,
                self.COLUMN_SIZE,
                size_item,
            )

            self._table.setItem(
                row,
                self.COLUMN_MODIFIED,
                modified_item,
            )

        self._table.setSortingEnabled(True)

    def selected_document(
        self,
    ) -> Document | None:
        """Return the currently selected document."""

        row = self._table.currentRow()

        if row < 0:
            return None

        item = self._table.item(
            row,
            self.COLUMN_NAME,
        )

        if item is None:
            return None

        return item.data(
            Qt.ItemDataRole.UserRole,
        )

    def clear(self) -> None:
        """Clear all table contents."""

        self._table.clearContents()
        self._table.setRowCount(0)

    @property
    def table(self) -> QTableWidget:
        """Return the underlying table widget."""

        return self._table
