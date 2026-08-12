"""
Workspace folder import service.

Coordinates recursive folder discovery and document import
while keeping the existing document and indexing services
as the underlying boundaries.
"""

from __future__ import annotations

from pathlib import Path

from athena.documents.import_report import (
    ImportReport,
)

from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)


class WorkspaceImportService:
    """
    High-level workspace folder import workflow.

    This service does not own documents or indexing.
    It coordinates the existing WorkspaceDocumentService.
    """

    def __init__(
        self,
        document_service: WorkspaceDocumentService,
    ) -> None:
        """
        Initialize the workspace import service.
        """

        self._documents = document_service

    def import_folder(
        self,
        folder: Path,
        force: bool = False,
    ) -> ImportReport:
        """
        Import all supported documents from a folder recursively.

        Args:
            folder:
                Root folder to scan.

            force:
                Force re-indexing of imported documents.

        Returns:
            ImportReport describing the operation.
        """

        sources = (
            self._documents.document_service.discover_documents(
                folder,
            )
        )

        report = ImportReport(
            source_folder=folder,
            discovered=len(sources),
        )

        for source in sources:
            try:
                imported = (
                    self._documents.import_document(
                        source,
                        force=force,
                    )
                )

                report.imported.append(
                    imported,
                )

                report.manifest[
                    imported
                ] = source.relative_to(
                    folder,
                )

            except Exception as exc:
                report.failed.append(
                    f"{source}: {exc}",
                )

        return report
