"""
Workspace backup models.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class WorkspaceBackupResult:
    """
    Result of a workspace backup operation.
    """

    archive_path: Path
    workspace_name: str
    created: datetime
    size_bytes: int


@dataclass(frozen=True)
class WorkspaceRestoreResult:
    """
    Result of a workspace restore operation.
    """

    workspace_path: Path
    workspace_name: str
    restored_files: int
