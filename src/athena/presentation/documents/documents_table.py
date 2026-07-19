"""
Documents table.
"""

from __future__ import annotations

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

    def __init__(self) -> None:
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

    @property
    def model(
        self,
    ) -> DocumentsTableModel:
        """Return the table model."""

        return self._model
