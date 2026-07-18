"""
Application bootstrap for Project Athena.
"""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication


class AthenaApplication(QApplication):
    """Main Qt application."""

    def __init__(self) -> None:
        super().__init__(sys.argv)

        self.setApplicationName("Athena")
        self.setApplicationVersion("0.1.0")
        self.setOrganizationName("Project Athena")
