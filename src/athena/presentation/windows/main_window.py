"""
Main application window.
"""

from PySide6.QtWidgets import (
    QListWidget,
    QMainWindow,
    QSplitter,
    QStatusBar,
)

from athena.presentation.pages.home_page import HomePage
from athena.presentation.navigation.navigation_widget import NavigationWidget


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Athena")

        self.resize(1400, 900)

        self._create_ui()

    def _create_ui(self) -> None:

        splitter = QSplitter()

        self.navigation = NavigationWidget()

        self.home = HomePage()

        splitter.addWidget(self.navigation)
        splitter.addWidget(self.home)

        splitter.setStretchFactor(1, 1)

        self.setCentralWidget(splitter)

        status = QStatusBar()

        status.showMessage("Ready")

        self.setStatusBar(status)
