"""
Document toolbar widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QWidget,
)


class DocumentToolbar(QWidget):
    """Toolbar for document operations."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize the toolbar."""

        super().__init__(parent)

        self.import_button = QPushButton("Import File")

        self.import_folder_button = QPushButton("Import Folder")

        self.delete_button = QPushButton("Delete")

        self.refresh_button = QPushButton("Refresh")

        self.open_folder_button = QPushButton("Open Folder")

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configure the toolbar."""

        layout = QHBoxLayout(self)

        layout.addWidget(
            self.import_button,
        )

        layout.addWidget(
            self.import_folder_button,
        )

        layout.addWidget(
            self.delete_button,
        )

        layout.addWidget(
            self.refresh_button,
        )

        layout.addStretch()

        layout.addWidget(
            self.open_folder_button,
        )

        self.setLayout(
            layout,
        )

    def set_enabled(
        self,
        enabled: bool,
    ) -> None:
        """Enable or disable all toolbar buttons."""

        self.import_button.setEnabled(
            enabled,
        )

        self.import_folder_button.setEnabled(
            enabled,
        )

        self.delete_button.setEnabled(
            enabled,
        )

        self.refresh_button.setEnabled(
            enabled,
        )

        self.open_folder_button.setEnabled(
            enabled,
        )
