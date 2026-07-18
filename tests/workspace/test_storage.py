from datetime import datetime
from pathlib import Path

from athena.workspace.constants import WORKSPACE_VERSION
from athena.workspace.models import Workspace
from athena.workspace.storage import WorkspaceStorage


def test_create_directories(tmp_path: Path):
    workspace = tmp_path / "Research"

    WorkspaceStorage.create_directories(workspace)

    assert workspace.exists()

    assert (workspace / "documents").exists()
    assert (workspace / "notes").exists()
    assert (workspace / "exports").exists()
    assert (workspace / "cache").exists()
    assert (workspace / "settings").exists()


def test_write_and_read_workspace(tmp_path: Path):
    workspace_path = tmp_path / "Research"

    WorkspaceStorage.create_directories(workspace_path)

    workspace = Workspace(
        name="Research",
        path=workspace_path,
        version=WORKSPACE_VERSION,
        created=datetime.now(),
        modified=datetime.now(),
    )

    WorkspaceStorage.write_workspace(workspace)

    loaded = WorkspaceStorage.read_workspace(workspace_path)

    assert loaded.name == workspace.name
    assert loaded.version == workspace.version
    assert loaded.path == workspace.path
