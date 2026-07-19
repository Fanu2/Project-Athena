"""
Documents table model.
"""

from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
)

from athena.documents.models import Document


class DocumentsTableModel(QAbstractTableModel):
    """Table model for workspace documents."""

    HEADERS = [
        "Name",
        "Type",
        "Size",
        "Modified",
    ]

    def __init__(self) -> None:
        super().__init__()

        self._documents: list[Document] = []

    def set_documents(
        self,
        documents: list[Document],
    ) -> None:
        """Replace the model contents."""

        self.beginResetModel()

        self._documents = sorted(
            documents,
            key=lambda document: document.path.name.lower(),
        )

        self.endResetModel()

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

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> object | None:
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return self.HEADERS[section]

        return None

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
                return document.path.name

            case 1:
                return document.path.suffix.lower()

            case 2:
                return f"{document.path.stat().st_size:,}"

            case 3:
                return datetime.fromtimestamp(
                    document.path.stat().st_mtime,
                ).strftime("%Y-%m-%d %H:%M")

        return None

    def document_at(
        self,
        row: int,
    ) -> Document:
        """Return the document at the specified row."""

        return self._documents[row]
