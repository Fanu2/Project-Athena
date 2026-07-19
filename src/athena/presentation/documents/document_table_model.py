"""
Qt table model for indexed documents.
"""

from __future__ import annotations

from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtCore import Qt

from athena.indexing.models import IndexedDocument


class DocumentTableModel(QAbstractTableModel):
    """Table model for indexed documents."""

    HEADERS = (
        "Title",
        "Pages",
        "Indexed",
        "Path",
    )

    def __init__(
        self,
        documents: list[IndexedDocument] | None = None,
    ) -> None:
        super().__init__()

        self._documents = documents or []

    def rowCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = QModelIndex(),
    ) -> int:
        if parent.isValid():
            return 0

        return len(self._documents)

    def columnCount(
        self,
        parent: QModelIndex | QPersistentModelIndex = QModelIndex(),
    ) -> int:
        if parent.isValid():
            return 0

        return len(self.HEADERS)

    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> object | None:
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None

        document = self._documents[index.row()]

        match index.column():
            case 0:
                return document.title

            case 1:
                return document.page_count

            case 2:
                return document.indexed_at.strftime(
                    "%Y-%m-%d %H:%M",
                )

            case 3:
                return str(document.path)

        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> object | None:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.HEADERS[section]

        return None

    def set_documents(
        self,
        documents: list[IndexedDocument],
    ) -> None:
        """Replace the model contents."""

        self.beginResetModel()

        self._documents = documents

        self.endResetModel()

    def document_at(
        self,
        row: int,
    ) -> IndexedDocument:
        """Return the document at the given row."""

        return self._documents[row]
