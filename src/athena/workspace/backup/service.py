"""
Workspace backup service.
"""

from __future__ import annotations

import zipfile
from datetime import datetime
from pathlib import Path

from ..models import Workspace

from .models import WorkspaceBackupResult


class WorkspaceBackupService:
    """
    Creates backups of Athena workspaces.
    """

    def export_workspace(
        self,
        workspace: Workspace,
        destination: Path,
    ) -> WorkspaceBackupResult:
        """
        Export a workspace into a ZIP archive.

        Args:
            workspace: Workspace to backup.
            destination: Output ZIP path.

        Returns:
            Backup result.
        """

        if not workspace.path.exists():
            raise FileNotFoundError(
                f"Workspace path does not exist: {workspace.path}"
            )

        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with zipfile.ZipFile(
            destination,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archive:

            for file_path in workspace.path.rglob("*"):
                if file_path.is_file():
                    archive.write(
                        file_path,
                        file_path.relative_to(
                            workspace.path.parent,
                        ),
                    )

        created = datetime.now()

        return WorkspaceBackupResult(
            archive_path=destination,
            workspace_name=workspace.name,
            created=created,
            size_bytes=destination.stat().st_size,
        )
