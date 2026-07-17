"""Business logic for Athena workspaces."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .constants import WORKSPACE_VERSION
from .exceptions import (
    InvalidWorkspaceError,
    WorkspaceExistsError,
)
from .models import Workspace
from .storage import WorkspaceStorage


class WorkspaceService:
    """Provides high-level workspace operations."""

    def __init__(self) -> None:
        self._storage = WorkspaceStorage()

    def create_workspace(self, parent: Path, name: str) -> Workspace:
        """
        Create a new workspace.

        Args:
            parent: Parent directory.
            name: Workspace name.

        Returns:
            Workspace instance.

        Raises:
            WorkspaceExistsError
        """

        workspace_path = parent / name

        if workspace_path.exists():
            raise WorkspaceExistsError(
                f"Workspace '{name}' already exists."
            )

        now = datetime.now()

        workspace = Workspace(
            name=name,
            path=workspace_path,
            version=WORKSPACE_VERSION,
            created=now,
            modified=now,
        )

        self._storage.create_directories(workspace_path)
        self._storage.write_workspace(workspace)

        return workspace

    def open_workspace(self, path: Path) -> Workspace:
        """Open an existing workspace."""

        if not self._storage.is_workspace(path):
            raise InvalidWorkspaceError(
                f"'{path}' is not an Athena workspace."
            )

        return self._storage.read_workspace(path)

    def save_workspace(self, workspace: Workspace) -> None:
        """Save workspace metadata."""

        workspace.modified = datetime.now()

        self._storage.write_workspace(workspace)

    def is_workspace(self, path: Path) -> bool:
        """Return True if path is a valid workspace."""

        return self._storage.is_workspace(path)