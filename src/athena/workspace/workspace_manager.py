"""
Runtime workspace manager.
"""

from __future__ import annotations

from pathlib import Path

from athena.services.workspace_document_service import (
    WorkspaceDocumentService,
)
from athena.services.workspace_query_service import (
    WorkspaceQueryService,
)

from .models import Workspace
from .service import WorkspaceService


class WorkspaceManager:
    """Coordinates the active Athena workspace."""

    def __init__(
        self,
        workspace_service: WorkspaceService,
        document_service: WorkspaceDocumentService,
        query_service: WorkspaceQueryService,
    ) -> None:
        """Initialize the runtime workspace manager."""

        self._workspace_service = workspace_service
        self._document_service = document_service
        self._query_service = query_service

        self._workspace: Workspace | None = None

    @property
    def workspace(self) -> Workspace | None:
        """Return the active workspace."""
        return self._workspace

    @property
    def is_open(self) -> bool:
        """Return True if a workspace is currently open."""
        return self._workspace is not None

    def create_workspace(
        self,
        parent: Path,
        name: str,
    ) -> Workspace:
        """Create and activate a workspace."""

        self._workspace = self._workspace_service.create_workspace(
            parent,
            name,
        )

        return self._workspace

    def open_workspace(
        self,
        path: Path,
    ) -> Workspace:
        """Open and activate an existing workspace."""

        self._workspace = self._workspace_service.open_workspace(
            path,
        )

        return self._workspace

    def save_workspace(self) -> None:
        """Save the active workspace."""

        if self._workspace is not None:
            self._workspace_service.save_workspace(
                self._workspace,
            )

    def close_workspace(self) -> None:
        """Close the active workspace."""

        self._workspace = None

    def list_documents(self):
        """Return workspace documents."""
        return self._document_service.list_documents()

    def library_summary(self):
        """Return workspace statistics."""
        return self._query_service.library_summary()

    def describe_library(self):
        """Return a human-readable library summary."""
        return self._query_service.describe_library()
