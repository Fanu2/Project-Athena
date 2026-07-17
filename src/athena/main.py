"""
Project Athena entry point.
"""

from __future__ import annotations

from athena.core.application import AthenaApplication
from athena.presentation.windows.main_window import MainWindow


def main() -> int:
    """Application entry point."""

    app = AthenaApplication()

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
