"""
Home page.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.workspace.models import Workspace


class HomePage(QWidget):
    """Application home page."""

    def __init__(self) -> None:
        super().__init__()

        self.title_label = QLabel("Welcome to Athena")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.workspace_label = QLabel("No workspace is currently open.")
        self.workspace_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.path_label = QLabel()
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)

        layout.addStretch()
        layout.addWidget(self.title_label)
        layout.addWidget(self.workspace_label)
        layout.addWidget(self.path_label)
        layout.addStretch()

    def set_workspace(
        self,
        workspace: Workspace,
    ) -> None:
        """Display the active workspace."""

        self.title_label.setText("Workspace")

        self.workspace_label.setText(workspace.name)

        self.path_label.setText(str(workspace.path))

    def clear_workspace(self) -> None:
        """Reset the page."""

        self.title_label.setText("Welcome to Athena")

        self.workspace_label.setText("No workspace is currently open.")

        self.path_label.clear()
