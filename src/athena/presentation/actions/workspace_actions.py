"""Workspace-related UI actions.

This module provides the presentation-layer bridge between
Athena UI components and workspace services.

UI code should call WorkspaceActions rather than directly
accessing domain services.
"""

from __future__ import annotations

from pathlib import Path

from athena.workspace.backup import (
    WorkspaceBackupResult,
    WorkspaceBackupService,
    WorkspaceRestoreResult,
    WorkspaceRestoreService,
)
from athena.workspace.models import Workspace
from athena.workspace.service import WorkspaceService


class WorkspaceActions:
    """
    Coordinates workspace actions between the UI
    and the service layer.

    Responsibilities:
    - Create/open/save workspaces
    - Validate workspace paths
    - Create workspace backups
    - Restore workspaces from backups

    This keeps presentation code independent from
    workspace implementation details.
    """

    def __init__(self) -> None:
        """
        Initialize workspace action handlers.

        WorkspaceService handles normal workspace
        lifecycle operations.

        Backup and restore services handle
        workspace recovery operations.
        """

        self._service = WorkspaceService()

        # A20.10:
        # Workspace backup support
        self._backup_service = WorkspaceBackupService()

        # A20.11:
        # Workspace restore support
        self._restore_service = WorkspaceRestoreService()

    def create_workspace(
        self,
        parent: Path,
        name: str,
    ) -> Workspace:
        """
        Create a new Athena workspace.

        Args:
            parent: Parent directory.
            name: Workspace name.

        Returns:
            Newly created Workspace object.
        """

        return self._service.create_workspace(
            parent,
            name,
        )

    def open_workspace(
        self,
        path: Path,
    ) -> Workspace:
        """
        Open an existing Athena workspace.

        Args:
            path: Workspace directory.

        Returns:
            Loaded Workspace object.
        """

        return self._service.open_workspace(
            path,
        )

    def save_workspace(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Save workspace metadata.

        Updates workspace persistence
        through WorkspaceService.
        """

        self._service.save_workspace(
            workspace,
        )

    def is_workspace(
        self,
        path: Path,
    ) -> bool:
        """
        Check whether a directory is a valid
        Athena workspace.
        """

        return self._service.is_workspace(
            path,
        )

    def backup_workspace(
        self,
        workspace: Workspace,
        destination: Path,
    ) -> WorkspaceBackupResult:
        """
        Create a workspace backup archive.

        A20.10:
        Exposes WorkspaceBackupService
        to the presentation layer.
        """

        return self._backup_service.export_workspace(
            workspace,
            destination,
        )

    def restore_workspace(
        self,
        archive_path: Path,
        destination: Path,
    ) -> WorkspaceRestoreResult:
        """
        Restore a workspace from a backup archive.

        A20.11:
        Exposes WorkspaceRestoreService
        to the presentation layer.
        """

        return self._restore_service.restore_workspace(
            archive_path,
            destination,
        )