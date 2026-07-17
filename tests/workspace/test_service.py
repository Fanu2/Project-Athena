from pathlib import Path

import pytest

from athena.workspace.exceptions import (
    InvalidWorkspaceError,
    WorkspaceExistsError,
)
from athena.workspace.service import WorkspaceService


def test_create_workspace(tmp_path: Path):
    service = WorkspaceService()

    workspace = service.create_workspace(
        tmp_path,
        "My Research",
    )

    assert workspace.name == "My Research"
    assert workspace.path.exists()


def test_duplicate_workspace(tmp_path: Path):
    service = WorkspaceService()

    service.create_workspace(tmp_path, "Research")

    with pytest.raises(WorkspaceExistsError):
        service.create_workspace(tmp_path, "Research")


def test_open_workspace(tmp_path: Path):
    service = WorkspaceService()

    created = service.create_workspace(
        tmp_path,
        "History",
    )

    loaded = service.open_workspace(created.path)

    assert loaded.name == created.name


def test_invalid_workspace(tmp_path: Path):
    service = WorkspaceService()

    folder = tmp_path / "Random"

    folder.mkdir()

    with pytest.raises(InvalidWorkspaceError):
        service.open_workspace(folder)