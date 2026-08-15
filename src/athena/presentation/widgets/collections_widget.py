"""
Collections widget.

Displays workspace collections.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QListWidget,
    QVBoxLayout,
    QWidget,
)

from athena.domain.collection import Collection


class CollectionsWidget(QWidget):
    """
    Widget for displaying collections.
    """

    collection_selected = Signal(object)

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._collections: list[Collection] = []

        self.list = QListWidget()

        self._setup_ui()

        self.list.currentRowChanged.connect(
            self._on_selection_changed,
        )

    def _setup_ui(self) -> None:
        """Build widget layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.list,
        )

        self.setLayout(
            layout,
        )

    def set_collections(
        self,
        collections: list[Collection],
    ) -> None:
        """
        Display collections.
        """

        self._collections = collections

        self.list.clear()

        for collection in collections:
            self.list.addItem(
                collection.name,
            )

    def selected_collection(
        self,
    ) -> Collection | None:
        """
        Return selected collection.
        """

        row = self.list.currentRow()

        if row < 0:
            return None

        return self._collections[row]

    def _on_selection_changed(
        self,
        row: int,
    ) -> None:
        """
        Emit selected collection.
        """

        if row < 0:
            self.collection_selected.emit(
                None,
            )

            return

        self.collection_selected.emit(
            self._collections[row],
        )