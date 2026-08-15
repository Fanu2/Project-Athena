"""
Collections widget.

Displays workspace collections and provides
UI events for collection management.

The widget does not own business logic.
It emits signals and lets the application
layer call CollectionService.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from athena.domain.collection import Collection


class CollectionsWidget(QWidget):
    """
    Widget for displaying workspace collections.
    """

    # Emitted when user selects a collection.
    collection_selected = Signal(object)

    # Request from UI to create a collection.
    # MainWindow/ApplicationContext handles it.
    create_collection_requested = Signal()

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._collections: list[Collection] = []

        self.list = QListWidget()

        self.create_button = QPushButton(
            "New Collection",
        )

        self._setup_ui()

        self.list.currentRowChanged.connect(
            self._on_selection_changed,
        )

        self.create_button.clicked.connect(
            self.create_collection_requested.emit,
        )

    def _setup_ui(self) -> None:
        """
        Build widget layout.
        """

        layout = QVBoxLayout(self)

        # Collection creation action.
        layout.addWidget(
            self.create_button,
        )

        # Collection list.
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
        Display available collections.
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