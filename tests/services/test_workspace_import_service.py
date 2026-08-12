"""
Tests for workspace folder import service.
"""

from pathlib import Path

from athena.documents.import_report import (
    ImportReport,
)

from athena.services.workspace_import_service import (
    WorkspaceImportService,
)


class FakeDocumentService:
    """
    Minimal workspace document service.
    """

    def __init__(
        self,
        imported: list[Path],
    ) -> None:
        self._imported = imported

        self.document_service = self

    def discover_documents(
        self,
        folder: Path,
    ) -> list[Path]:
        return self._imported

    def import_document(
        self,
        source: Path,
        force: bool = False,
    ) -> Path:
        return source


def test_import_folder_creates_report(
    tmp_path: Path,
) -> None:

    documents = [
        tmp_path / "one.pdf",
        tmp_path / "two.html",
    ]

    service = WorkspaceImportService(
        FakeDocumentService(
            documents,
        ),
    )

    report = service.import_folder(
        tmp_path,
    )

    assert isinstance(
        report,
        ImportReport,
    )

    assert report.source_folder == tmp_path

    assert report.discovered == 2

    assert report.imported_count == 2

    assert report.failed_count == 0

    assert report.imported == documents

    assert report.manifest[
        documents[0]
    ] == Path(
        "one.pdf",
    )

    assert report.manifest[
        documents[1]
    ] == Path(
        "two.html",
    )
