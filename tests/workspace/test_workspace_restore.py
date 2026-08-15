"""
Tests for workspace restore service.
"""

from datetime import datetime
from pathlib import Path

from athena.workspace.models import Workspace
from athena.workspace.storage import WorkspaceStorage
from athena.workspace.backup import (
    WorkspaceBackupService,
    WorkspaceRestoreService,
)


def test_workspace_restore_creates_workspace(
    tmp_path: Path,
) -> None:
    """
    Restore should recreate a valid Athena workspace.
    """

    original = tmp_path / "original"

    storage = WorkspaceStorage()

    storage.create_directories(
        original,
    )

    workspace = Workspace(
        name="demo",
        path=original,
        version="0.1.0",
        created=datetime.now(),
        modified=datetime.now(),
        description="",
        metadata={},
    )

    storage.write_workspace(
        workspace,
    )

    document = original / "documents" / "test.md"

    document.write_text(
        "# Restore Test",
        encoding="utf-8",
    )

    backup = tmp_path / "backup.zip"

    WorkspaceBackupService().export_workspace(
        workspace,
        backup,
    )

    restored = tmp_path / "restored"

    result = WorkspaceRestoreService().restore_workspace(
        backup,
        restored,
    )

    assert result.workspace_name == "demo"
    assert result.restored_files > 0

    assert (
        restored / "workspace.json"
    ).exists()

    assert (
        restored / "documents" / "test.md"
    ).exists()


def test_workspace_restore_rejects_invalid_archive(
    tmp_path: Path,
) -> None:
    """
    Restore should reject archives without workspace.json.
    """

    import zipfile

    invalid = tmp_path / "invalid.zip"

    with zipfile.ZipFile(
        invalid,
        "w",
    ) as archive:
        archive.writestr(
            "random.txt",
            "invalid",
        )

    destination = tmp_path / "restore"

    try:
        WorkspaceRestoreService().restore_workspace(
            invalid,
            destination,
        )
        assert False
    except ValueError:
        assert True
