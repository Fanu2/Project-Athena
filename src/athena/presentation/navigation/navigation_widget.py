"""
Left navigation panel.
"""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QListWidget


class NavigationWidget(QListWidget):
    """Application navigation."""

    home_selected = Signal()
    documents_selected = Signal()
    search_selected = Signal()
    settings_selected = Signal()

    def __init__(self) -> None:
        """Initialize the navigation widget."""

        super().__init__()

        self.setMaximumWidth(220)

        self.addItem("🏠 Home")
        self.addItem("📄 Documents")
        self.addItem("🔍 Search")
        self.addItem("⚙ Settings")

        self.setCurrentRow(0)

        self.currentRowChanged.connect(
            self._on_current_row_changed,
        )

    def _on_current_row_changed(
        self,
        row: int,
    ) -> None:
        """Handle navigation selection."""

        match row:
            case 0:
                self.home_selected.emit()

            case 1:
                self.documents_selected.emit()

            case 2:
                self.search_selected.emit()

            case 3:
                self.settings_selected.emit()
