"""
Workspace metadata helpers.
"""

from __future__ import annotations

from pathlib import Path

from .models import Workspace


def apply_import_source_metadata(
    workspace: Workspace,
    source_folder: Path,
) -> Workspace:
    """
    Record folder import source information.

    Does not modify workspace storage.
    """

    workspace.metadata.update(
        {
            "source_type": "folder_import",
            "source_folder": source_folder.name,
        }
    )

    return workspace
