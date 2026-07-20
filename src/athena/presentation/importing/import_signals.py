"""
Signals used by the background import worker.
"""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal


class ImportSignals(QObject):
    """Qt signals emitted during document import."""

    started = Signal(int)
    """Total number of files to import."""

    current_file = Signal(str)
    """Filename currently being processed."""

    status = Signal(str)
    """Current import status."""

    progress = Signal(int, int)
    """Current progress (current, total)."""

    file_finished = Signal(str)
    """Successfully imported filename."""

    file_failed = Signal(str, str)
    """Filename and error message."""

    finished = Signal(object)
    """Import summary object."""