"""
Left navigation panel.
"""

from PySide6.QtWidgets import QListWidget


class NavigationWidget(QListWidget):
    """Application navigation."""

    def __init__(self) -> None:
        super().__init__()

        self.setMaximumWidth(220)

        self.addItem("🏠 Home")
        self.addItem("📁 Workspace")
        self.addItem("⚙ Settings")