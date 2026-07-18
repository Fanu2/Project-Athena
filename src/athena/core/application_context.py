"""
Application context.

Creates and owns shared application services.
"""

from __future__ import annotations

from pathlib import Path

from athena.documents.service import DocumentService
from athena.indexing.repositories.memory import (
    MemoryChunkRepository,
)
from athena.indexing.service import IndexingService
from athena.presentation.actions.workspace_actions import (
    WorkspaceActions,
)


class ApplicationContext:
    """Owns application-wide services."""

    def __init__(self) -> None:
        """Initialize application services."""

        self.workspace_actions = WorkspaceActions()

        self.document_service: DocumentService | None = None

        self.chunk_repository = MemoryChunkRepository()

        self.indexing_service = IndexingService(
            self.chunk_repository,
        )

    def open_workspace(
        self,
        workspace_path: Path,
    ) -> None:
        """Initialize workspace-specific services."""

        self.document_service = DocumentService(
            workspace_path / "documents",
        )

    def close_workspace(self) -> None:
        """Release workspace-specific services."""

        self.document_service = None
