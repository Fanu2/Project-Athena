"""
Main application window.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Athena")
        self.resize(1400, 900)

        label = QLabel("Welcome to Project Athena")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)