"""
Tests for workspace import preview service.
"""

from pathlib import Path

from athena.services.workspace_import_preview_service import (
    WorkspaceImportPreviewService,
)


def test_preview_scans_folder(
    tmp_path: Path,
) -> None:

    (tmp_path / "record.pdf").write_text(
        "pdf",
    )

    (tmp_path / "owners.xlsx").write_text(
        "xlsx",
    )

    (tmp_path / "notes.xyz").write_text(
        "unsupported",
    )

    service = (
        WorkspaceImportPreviewService()
    )

    preview = service.preview(
        tmp_path,
    )

    assert (
        preview.supported_count
        == 2
    )

    assert (
        preview.unsupported_count
        == 1
    )

    assert (
        preview.file_types[".pdf"]
        == 1
    )

    assert (
        preview.file_types[".xlsx"]
        == 1
    )
