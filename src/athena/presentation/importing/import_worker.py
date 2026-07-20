"""
Background document import worker.
"""

from __future__ import annotations

import time
from pathlib import Path

from athena.presentation.importing.import_signals import (
    ImportSignals,
)
from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)


class ImportWorker:
    """Imports and indexes documents."""

    def __init__(
        self,
        document_service: WorkspaceDocumentService,
        documents: list[Path],
    ) -> None:
        self._document_service = document_service
        self._documents = documents

        self.signals = ImportSignals()

    def run(self) -> None:
        """Import all documents."""

        total = len(self._documents)

        imported = 0
        failed = 0
        skipped = 0

        start_time = time.perf_counter()

        self.signals.started.emit(total)

        for index, document in enumerate(self._documents, start=1):

            self.signals.current_file.emit(
                document.name,
            )

            self.signals.status.emit(
                "Importing document...",
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

        self.signals.finished.emit(
            summary,
        )