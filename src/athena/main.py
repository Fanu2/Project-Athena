"""
Project Athena entry point.
"""

from __future__ import annotations

from athena.core.application import AthenaApplication
from athena.core.application_context import ApplicationContext
from athena.presentation.windows.main_window import MainWindow


def main() -> int:
    """Application entry point."""

    app = AthenaApplication()

    # Create shared application services.
    context = ApplicationContext()

    # Create and show the main window.
    window = MainWindow(context)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
