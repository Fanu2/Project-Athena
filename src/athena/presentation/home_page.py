"""
Home page.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class HomePage(QWidget):
    """Athena home page."""

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("Welcome to Project Athena")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        new_button = QPushButton("New Workspace")

        open_button = QPushButton("Open Workspace")

        layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(new_button)
        layout.addWidget(open_button)

        layout.addStretch()

        self.setLayout(layout)