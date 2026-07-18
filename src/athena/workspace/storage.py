"""Filesystem storage for Athena workspaces."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .constants import DEFAULT_FOLDERS, WORKSPACE_FILE
from .exceptions import InvalidWorkspaceError
from .models import Workspace


class WorkspaceStorage:
    """Handles reading and writing workspace data."""

    @staticmethod
    def create_directories(path: Path) -> None:
        """Create the standard workspace directory structure."""
        path.mkdir(parents=True, exist_ok=True)

        for folder in DEFAULT_FOLDERS:
            (path / folder).mkdir(exist_ok=True)

    @staticmethod
    def write_workspace(workspace: Workspace) -> None:
        """Write workspace metadata to workspace.json."""
        data = {
            "name": workspace.name,
            "version": workspace.version,
            "created": workspace.created.isoformat(),
            "modified": workspace.modified.isoformat(),
        }

        with open(workspace.path / WORKSPACE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def read_workspace(path: Path) -> Workspace:
        """Read workspace metadata from disk."""
        workspace_file = path / WORKSPACE_FILE

        if not workspace_file.exists():
            raise InvalidWorkspaceError(f"No workspace found at '{path}'.")

        with open(workspace_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        return Workspace(
            name=data["name"],
            path=path,
            version=data["version"],
            created=datetime.fromisoformat(data["created"]),
            modified=datetime.fromisoformat(data["modified"]),
        )

    @staticmethod
    def is_workspace(path: Path) -> bool:
        """Return True if the directory contains a valid Athena workspace."""
        return (path / WORKSPACE_FILE).is_file()
