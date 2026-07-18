"""
Search results model.
"""

from __future__ import annotations

from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)

from athena.indexing.models import DocumentChunk


class SearchResultsModel(QAbstractListModel):
    """Qt model for displaying search results."""

    def __init__(self) -> None:
        super().__init__()

        self._results: list[DocumentChunk] = []

    def set_results(
        self,
        results: list[DocumentChunk],
    ) -> None:
        """Replace search results."""

        self.beginResetModel()

        self._results = results

        self.endResetModel()

    def get_chunk(
        self,
        row: int,
    ) -> DocumentChunk | None:
        """Return chunk by row."""

        if row < 0 or row >= len(self._results):
            return None

        return self._results[row]

    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = QModelIndex(),
    ) -> int:
        """Return number of results."""

        return len(self._results)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        """Return display data."""

        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            chunk = self._results[index.row()]

            preview = chunk.text[:120]

            return f"Page {chunk.page_number}\n" f"{preview}"

        return None
