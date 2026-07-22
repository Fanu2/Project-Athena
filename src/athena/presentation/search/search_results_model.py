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

        self._query: str = ""

    def set_results(
        self,
        results: list[DocumentChunk],
        query: str = "",
    ) -> None:
        """Replace search results."""

        self.beginResetModel()

        self._results = results
        self._query = query.strip()

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

            preview = self._create_preview(
                chunk.text,
            )

            return f"Page {chunk.page_number}\n{preview}"

        return None

    def _create_preview(
        self,
        text: str,
        length: int = 120,
    ) -> str:
        """Create a readable search preview."""

        if not self._query:
            return text[:length]

        lower_text = text.lower()

        position = lower_text.find(
            self._query.lower(),
        )

        if position == -1:
            return text[:length]

        start = max(
            0,
            position - 40,
        )

        end = min(
            len(text),
            position + length,
        )

        preview = text[start:end]

        if start > 0:
            preview = "... " + preview

        if end < len(text):
            preview += " ..."

        return preview
