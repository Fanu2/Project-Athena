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
