"""
Background document import worker.
"""

from __future__ import annotations

import time
from pathlib import Path

from PySide6.QtCore import QObject, Slot

from athena.presentation.importing.import_signals import (
    ImportSignals,
)
from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)


class ImportWorker(QObject):
    """Background worker for importing and indexing documents."""

    def __init__(
        self,
        document_service: WorkspaceDocumentService,
        documents: list[Path],
    ) -> None:
        """Initialize the import worker."""
        super().__init__()

        self._document_service = document_service
        self._documents = documents

        self._cancel_requested = False

        self.signals = ImportSignals()

    @Slot()
    def cancel(self) -> None:
        """Request cancellation of the import process."""

        self._cancel_requested = True

    @Slot()
    def run(self) -> None:
        """Import and index all documents."""

        total = len(self._documents)

        imported = 0
        skipped = 0
        failed = 0

        start_time = time.perf_counter()

        self.signals.started.emit(total)

        for index, document in enumerate(
            self._documents,
            start=1,
        ):
            if self._cancel_requested:
                self.signals.status.emit(
                    "Cancelling import..."
                )

                self.signals.cancelled.emit()
                return

            self.signals.current_file.emit(
                document.name,
            )

            self.signals.status.emit(
                "Importing document..."
            )

            try:
                self._document_service.import_document(
                    document,
                )

                imported += 1

                self.signals.file_finished.emit(
                    document.name,
                )

            except Exception as exc:
                failed += 1

                self.signals.file_failed.emit(
                    document.name,
                    str(exc),
                )

            self.signals.progress.emit(
                index,
                total,
            )

        elapsed = time.perf_counter() - start_time

        summary = {
            "total": total,
            "imported": imported,
            "skipped": skipped,
            "failed": failed,
            "elapsed": elapsed,
        }

        self.signals.finished.emit(summary)