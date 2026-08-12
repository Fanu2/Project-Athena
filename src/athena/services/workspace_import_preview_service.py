"""
Workspace import preview service.

Scans folders and produces an import summary
without modifying workspace data.
"""

from __future__ import annotations

from pathlib import Path

from athena.documents.import_preview import (
    ImportPreview,
)

from athena.documents.folder_importer import (
    FolderImporter,
)


class WorkspaceImportPreviewService:
    """
    Creates previews before workspace import.

    This service only scans.
    It does not copy, index, or modify documents.
    """

    def __init__(
        self,
        folder_importer: FolderImporter | None = None,
    ) -> None:
        """
        Initialize preview service.
        """

        self._folder_importer = (
            folder_importer
            if folder_importer is not None
            else FolderImporter()
        )

    def preview(
        self,
        folder: Path,
    ) -> ImportPreview:
        """
        Scan a folder and create an import preview.
        """

        supported = (
            self._folder_importer.discover_documents(
                folder,
            )
        )

        all_files = [
            path
            for path in folder.rglob("*")
            if path.is_file()
        ]

        unsupported_count = (
            len(all_files)
            - len(supported)
        )

        file_types: dict[str, int] = {}

        for document in supported:
            extension = (
                document.suffix.lower()
            )

            file_types[extension] = (
                file_types.get(extension, 0)
                + 1
            )

        return ImportPreview(
            source_folder=folder,
            supported_files=tuple(
                supported,
            ),
            unsupported_count=unsupported_count,
            file_types=file_types,
        )
