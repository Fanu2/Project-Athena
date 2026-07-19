"""
Documents table.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import (
    QModelIndex,
    Signal,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableView,
)

from athena.presentation.documents.documents_table_model import (
    DocumentsTableModel,
)


class DocumentsTable(QTableView):
    """Table displaying workspace documents."""

    document_activated = Signal(Path)

    def __init__(self) -> None:
        """Initialize the documents table."""

        super().__init__()

        self._model = DocumentsTableModel()

        self.setModel(
            self._model,
        )

        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows,
        )

        self.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection,
        )

        self.setAlternatingRowColors(
            True,
        )

        self.setSortingEnabled(
            False,
        )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers,
        )

        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch,
        )

        self.verticalHeader().setVisible(
            False,
        )

        self.doubleClicked.connect(
            self._on_double_clicked,
        )

    @property
    def table_model(
        self,
    ) -> DocumentsTableModel:
        """Return the table model."""

        return self._model

    def _on_double_clicked(
        self,
        index: QModelIndex,
    ) -> None:
        """Handle document activation."""

        if not index.isValid():
            return

        document = self._model.document_at(
            index.row(),
        )

        self.document_activated.emit(
            document.path,
        )