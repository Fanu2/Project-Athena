"""
AI Control Center page.

Displays Athena AI runtime information.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)


class AIControlCenterPage(QWidget):
    """Manage Athena AI runtime."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize AI Control Center."""

        super().__init__(parent)

        layout = QVBoxLayout(self)

        title = QLabel(
            "AI Control Center"
        )

        layout.addWidget(title)

        self.status = QLabel(
            "AI Runtime Ready"
        )

        layout.addWidget(self.status)