"""
Tests for workspace backup service.
"""

from pathlib import Path
from datetime import datetime

from athena.workspace.models import Workspace
from athena.workspace.backup import WorkspaceBackupService


def test_workspace_backup_creates_archive(
    tmp_path: Path,
) -> None:
    """
    Backup should create a ZIP containing workspace files.
    """

    workspace_path = tmp_path / "demo"

    workspace_path.mkdir()

    document = workspace_path / "documents"
    document.mkdir()

    test_file = document / "test.md"
    test_file.write_text(
        "# Athena Test",
        encoding="utf-8",
    )

    workspace = Workspace(
        name="demo",
        path=workspace_path,
        version="0.1.0",
        created=datetime.now(),
        modified=datetime.now(),
        description="",
        metadata={},
    )

    backup_path = tmp_path / "backup.zip"

    result = WorkspaceBackupService().export_workspace(
        workspace,
        backup_path,
    )

    assert result.archive_path == backup_path
    assert backup_path.exists()
    assert result.size_bytes > 0
