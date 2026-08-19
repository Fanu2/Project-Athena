from datetime import datetime
from pathlib import Path

from athena.workspace.constants import WORKSPACE_VERSION
from athena.workspace.models import Workspace
from athena.workspace.storage import WorkspaceStorage


def test_create_directories(
    tmp_path: Path,
) -> None:
    """
    Workspace directory structure is created.
    """

    workspace = tmp_path / "Research"

    WorkspaceStorage.create_directories(
        workspace,
    )

    assert workspace.exists()

    assert (workspace / "documents").exists()
    assert (workspace / "notes").exists()
    assert (workspace / "exports").exists()
    assert (workspace / "cache").exists()
    assert (workspace / "settings").exists()


def test_write_and_read_workspace(
    tmp_path: Path,
) -> None:
    """
    Workspace metadata survives write/read cycle.
    """

    workspace_path = tmp_path / "Research"

    WorkspaceStorage.create_directories(
        workspace_path,
    )

    workspace = Workspace(
        name="Research",
        path=workspace_path,
        version=WORKSPACE_VERSION,
        created=datetime.now(),
        modified=datetime.now(),
        description="Research workspace",
        metadata={
            "type": "knowledge",
        },
    )

    WorkspaceStorage.write_workspace(
        workspace,
    )

    loaded = WorkspaceStorage.read_workspace(
        workspace_path,
    )

    assert loaded.name == workspace.name

    assert loaded.version == workspace.version

    assert loaded.path == workspace.path

    assert loaded.workspace_id == workspace.workspace_id

    assert loaded.description == (
        workspace.description
    )

    assert loaded.metadata == (
        workspace.metadata
    )


def test_read_legacy_workspace_without_intelligence_fields(
    tmp_path: Path,
) -> None:
    """
    Legacy workspace.json files remain compatible.
    """

    workspace_path = tmp_path / "Legacy"

    workspace_path.mkdir()

    workspace_file = (
        workspace_path / "workspace.json"
    )

    workspace_file.write_text(
        """
        {
            "name": "Legacy",
            "version": "1.0",
            "created": "2026-01-01T00:00:00",
            "modified": "2026-01-01T00:00:00"
        }
        """,
        encoding="utf-8",
    )

    loaded = WorkspaceStorage.read_workspace(
        workspace_path,
    )

    assert loaded.name == "Legacy"

    assert loaded.version == "1.0"

    assert loaded.workspace_id is not None

    reloaded = WorkspaceStorage.read_workspace(
        workspace_path,
    )

    assert reloaded.workspace_id == loaded.workspace_id

    assert loaded.description == ""

    assert loaded.metadata == {}
