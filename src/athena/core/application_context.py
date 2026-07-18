"""
Application context.

Creates and owns shared application services.
"""

from __future__ import annotations

from pathlib import Path

from athena.documents.service import DocumentService
from athena.indexing.repositories.sqlite import SQLiteChunkRepository
from athena.indexing.service import IndexingService
from athena.presentation.actions.workspace_actions import (
    WorkspaceActions,
)
from athena.search.search_service import SearchService
from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)


class ApplicationContext:
    """Owns application-wide services."""

    def __init__(self) -> None:
        """Initialize application services."""

        self.workspace_actions = WorkspaceActions()

        self.indexing_service: IndexingService | None = None

        self.search_service: SearchService | None = None

        self.document_service: WorkspaceDocumentService | None = None

    def open_workspace(
        self,
        workspace_path: Path,
    ) -> None:
        """Initialize workspace-specific services."""

        athena_directory = workspace_path / ".athena"

        athena_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        chunk_repository = SQLiteChunkRepository(
            athena_directory / "index.db",
        )

        self.indexing_service = IndexingService(
            chunk_repository,
        )

        self.search_service = SearchService(
            chunk_repository,
        )

        document_service = DocumentService(
            workspace_path / "documents",
        )

        self.document_service = WorkspaceDocumentService(
            document_service=document_service,
            indexing_service=self.indexing_service,
        )

    def close_workspace(self) -> None:
        """Release workspace-specific services."""

        self.document_service = None

        self.indexing_service = None

        self.search_service = None
