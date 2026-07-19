"""
Documents toolbar.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
)


class DocumentsToolbar(QWidget):
    """Toolbar for managing workspace documents."""

    import_file_requested = Signal()

    import_folder_requested = Signal()

    remove_requested = Signal()

    refresh_requested = Signal()

    def __init__(self) -> None:
        """Initialize the toolbar."""

        super().__init__()

        self.import_file_button = QPushButton(
            "📄 Import File",
        )

        self.import_folder_button = QPushButton(
            "📂 Import Folder",
        )

        self.remove_button = QPushButton(
            "🗑 Remove",
        )

        self.refresh_button = QPushButton(
            "🔄 Refresh",
        )

        layout = QHBoxLayout(self)

        layout.addWidget(
            self.import_file_button,
        )

        layout.addWidget(
            self.import_folder_button,
        )

        layout.addStretch()

        layout.addWidget(
            self.remove_button,
        )

        layout.addWidget(
            self.refresh_button,
        )

        self.import_file_button.clicked.connect(
            self.import_file_requested.emit,
        )

        self.import_folder_button.clicked.connect(
            self.import_folder_requested.emit,
        )

        self.remove_button.clicked.connect(
            self.remove_requested.emit,
        )

        self.refresh_button.clicked.connect(
            self.refresh_requested.emit,
        )
