"""
Workspace restore service.
"""

from __future__ import annotations

import zipfile
from pathlib import Path

from ..storage import WorkspaceStorage

from .models import WorkspaceRestoreResult


class WorkspaceRestoreService:
    """
    Restores Athena workspaces from backup archives.
    """

    def __init__(self) -> None:
        self._storage = WorkspaceStorage()

    def restore_workspace(
        self,
        archive_path: Path,
        destination: Path,
    ) -> WorkspaceRestoreResult:
        """
        Restore an Athena workspace from a ZIP archive.

        Supports archives containing either:

            workspace.json
            documents/

        or:

            workspace_name/
                workspace.json
                documents/
        """

        if not archive_path.exists():
            raise FileNotFoundError(
                f"Backup not found: {archive_path}"
            )

        restored_files = 0

        with zipfile.ZipFile(
            archive_path,
            "r",
        ) as archive:

            files = [
                member
                for member in archive.infolist()
                if not member.is_dir()
            ]

            workspace_files = {
                Path(member.filename).name
                for member in files
            }

            if "workspace.json" not in workspace_files:
                raise ValueError(
                    "Backup archive does not contain a valid Athena workspace."
                )

            roots = {
                Path(member.filename).parts[0]
                for member in files
                if Path(member.filename).parts
            }

            prefix = None

            if len(roots) == 1:
                candidate = next(iter(roots))

                if candidate != "workspace.json":
                    prefix = candidate

            destination.mkdir(
                parents=True,
                exist_ok=True,
            )

            for member in files:

                relative_path = Path(
                    member.filename
                )

                if (
                    prefix
                    and relative_path.parts[0]
                    == prefix
                ):
                    relative_path = Path(
                        *relative_path.parts[1:]
                    )

                target = (
                    destination
                    / relative_path
                )

                target.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                with archive.open(
                    member
                ) as source:

                    target.write_bytes(
                        source.read()
                    )

                restored_files += 1

        if not self._storage.is_workspace(
            destination,
        ):
            raise ValueError(
                "Restored data is not a valid Athena workspace."
            )

        workspace = self._storage.read_workspace(
            destination,
        )

        return WorkspaceRestoreResult(
            workspace_path=destination,
            workspace_name=workspace.name,
            restored_files=restored_files,
        )
