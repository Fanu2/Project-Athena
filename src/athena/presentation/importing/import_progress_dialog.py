"""
Import progress dialog.
"""

from __future__ import annotations

from time import perf_counter
from typing import Any

from PySide6.QtCore import (
    Qt,
    QTimer,
)
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
)


class ImportProgressDialog(QDialog):
    """Dialog displaying document import progress."""

    def __init__(
        self,
        parent=None,
    ) -> None:
        """Initialize the dialog."""

        super().__init__(parent)

        self.setWindowTitle(
            "Importing Documents",
        )

        self.setModal(True)

        self.resize(
            500,
            240,
        )

        #
        # Timer
        #

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(
            self._update_elapsed,
        )

        self._start_time = 0.0

        self._build_ui()

    def _build_ui(self) -> None:
        """Create the dialog user interface."""

        layout = QVBoxLayout(self)

        #
        # Overall progress
        #

        layout.addWidget(
            QLabel(
                "Overall Progress",
            ),
        )

        self.progress_bar = QProgressBar()

        self.progress_bar.setRange(
            0,
            100,
        )

        self.progress_bar.setValue(
            0,
        )

        layout.addWidget(
            self.progress_bar,
        )

        #
        # Current file
        #

        layout.addWidget(
            QLabel(
                "Current File",
            ),
        )

        self.current_file_label = QLabel(
            "-",
        )

        self.current_file_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse,
        )

        layout.addWidget(
            self.current_file_label,
        )

        #
        # Status
        #

        layout.addWidget(
            QLabel(
                "Status",
            ),
        )

        self.status_label = QLabel(
            "Waiting...",
        )

        layout.addWidget(
            self.status_label,
        )

        #
        # Elapsed time
        #

        layout.addWidget(
            QLabel(
                "Elapsed Time",
            ),
        )

        self.elapsed_label = QLabel(
            "00:00",
        )

        layout.addWidget(
            self.elapsed_label,
        )

        #
        # Buttons
        #

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        self.cancel_button = QPushButton(
            "Cancel",
        )

        # ImportManager owns the cancellation workflow.

        button_layout.addWidget(
            self.cancel_button,
        )

        layout.addLayout(
            button_layout,
        )

    # ---------------------------------------------------------
    # Timer API
    # ---------------------------------------------------------

    def start_timer(self) -> None:
        """Start the elapsed timer."""

        self._start_time = perf_counter()

        self._update_elapsed()

        self._timer.start()

    def stop_timer(self) -> None:
        """Stop the elapsed timer."""

        self._timer.stop()

    def _update_elapsed(self) -> None:
        """Refresh the elapsed time."""

        elapsed = perf_counter() - self._start_time

        self.set_elapsed(
            elapsed,
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def set_total(
        self,
        total: int,
    ) -> None:
        """Initialize the progress bar."""

        self.progress_bar.setRange(
            0,
            max(
                total,
                1,
            ),
        )

        self.progress_bar.setValue(
            0,
        )

    def set_progress(
        self,
        current: int,
        total: int,
    ) -> None:
        """Update the progress bar."""

        self.progress_bar.setMaximum(
            max(
                total,
                1,
            ),
        )

        self.progress_bar.setValue(
            current,
        )

    def set_current_file(
        self,
        filename: str,
    ) -> None:
        """Display the current file."""

        self.current_file_label.setText(
            filename,
        )

    def set_status(
        self,
        text: str,
    ) -> None:
        """Display the current status."""

        self.status_label.setText(
            text,
        )

    def set_elapsed(
        self,
        seconds: float,
    ) -> None:
        """Update elapsed time."""

        total_seconds = int(seconds)

        minutes = total_seconds // 60
        secs = total_seconds % 60

        self.elapsed_label.setText(
            f"{minutes:02}:{secs:02}",
        )

    def set_finished(
        self,
        summary: dict[str, Any],
    ) -> None:
        """
        Display completion information.

        The dialog itself does not decide whether to close.
        ImportManager controls the workflow.
        """

        self.stop_timer()

        self.set_status(
            "Import completed.",
        )

        self.set_elapsed(
            summary.get(
                "elapsed",
                0.0,
            ),
        )
