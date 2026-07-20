"""
Import manager.

Coordinates asynchronous document imports using ImportWorker,
QThread, and ImportProgressDialog.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QWidget

from athena.presentation.importing.import_progress_dialog import (
    ImportProgressDialog,
)
from athena.presentation.importing.import_worker import (
    ImportWorker,
)
from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)


class ImportManager:
    """Coordinates asynchronous document imports."""

    def __init__(self) -> None:
        self._thread: QThread | None = None
        self._worker: ImportWorker | None = None
        self._dialog: ImportProgressDialog | None = None

    def import_documents(
        self,
        *,
        parent: QWidget,
        document_service: WorkspaceDocumentService,
        documents: list[Path],
        refresh_callback: Callable[[], None],
    ) -> None:
        """
        Import documents asynchronously.
        """

        if not documents:
            return

        self._dialog = ImportProgressDialog(parent)

        self._thread = QThread(parent)

        self._worker = ImportWorker(
            document_service=document_service,
            documents=documents,
        )

        self._worker.moveToThread(
            self._thread,
        )

        #
        # Thread lifecycle
        #

        self._thread.started.connect(
            self._worker.run,
        )

        self._worker.signals.finished.connect(
            self._on_finished,
        )

        self._worker.signals.finished.connect(
            refresh_callback,
        )

        self._worker.signals.finished.connect(
            self._thread.quit,
        )

        self._worker.signals.cancelled.connect(
            self._on_cancelled,
        )

        self._worker.signals.cancelled.connect(
            refresh_callback,
        )

        self._worker.signals.cancelled.connect(
            self._thread.quit,
        )

        self._thread.finished.connect(
            self._worker.deleteLater,
        )

        self._thread.finished.connect(
            self._thread.deleteLater,
        )

        #
        # Progress updates
        #

        self._worker.signals.started.connect(
            self._dialog.set_total,
        )

        self._worker.signals.current_file.connect(
            self._dialog.set_current_file,
        )

        self._worker.signals.status.connect(
            self._dialog.set_status,
        )

        self._worker.signals.progress.connect(
            self._dialog.set_progress,
        )

        #
        # Cancellation
        #

        self._dialog.cancel_button.clicked.connect(
            self._worker.cancel,
        )

        #
        # Start
        #

        self._dialog.start_timer()

        self._thread.start()

        self._dialog.exec()

        #
        # Ensure thread shutdown
        #

        if self._thread.isRunning():
            self._thread.quit()
            self._thread.wait()

        #
        # Release references
        #

        self._worker = None
        self._thread = None
        self._dialog = None

    # ---------------------------------------------------------
    # Internal slots
    # ---------------------------------------------------------

    def _on_finished(
        self,
        summary: dict[str, Any],
    ) -> None:
        """Handle successful completion."""

        if self._dialog is None:
            return

        self._dialog.set_finished(
            summary,
        )

        self._dialog.accept()

    def _on_cancelled(self) -> None:
        """Handle user cancellation."""

        if self._dialog is None:
            return

        self._dialog.stop_timer()

        self._dialog.set_status(
            "Import cancelled.",
        )

        self._dialog.reject()