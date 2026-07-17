"""Workspace-related UI actions."""

from __future__ import annotations

from pathlib import Path

from athena.workspace.models import Workspace
from athena.workspace.service import WorkspaceService


class WorkspaceActions:
    """Coordinates workspace actions between the UI and service layer."""

    def __init__(self) -> None:
        self._service = WorkspaceService()

    def create_workspace(self, parent: Path, name: str) -> Workspace:
        """Create a new workspace."""
        return self._service.create_workspace(parent, name)

    def open_workspace(self, path: Path) -> Workspace:
        """Open an existing workspace."""
        return self._service.open_workspace(path)

    def save_workspace(self, workspace: Workspace) -> None:
        """Save the current workspace."""
        self._service.save_workspace(workspace)

    def is_workspace(self, path: Path) -> bool:
        """Check whether a folder is an Athena workspace."""
        return self._service.is_workspace(path)