"""
Tests for workspace metadata helpers.
"""

from datetime import datetime
from pathlib import Path

from athena.workspace.metadata import (
    apply_import_source_metadata,
)

from athena.workspace.models import (
    Workspace,
)


def test_apply_import_source_metadata(
    tmp_path: Path,
) -> None:

    workspace = Workspace(
        name="Test",
        path=tmp_path,
        version="1.0",
        created=datetime.now(),
        modified=datetime.now(),
    )

    apply_import_source_metadata(
        workspace,
        Path("/data/Sirsa_Records"),
    )

    assert (
        workspace.metadata["source_type"]
        == "folder_import"
    )

    assert (
        workspace.metadata["source_folder"]
        == "Sirsa_Records"
    )
