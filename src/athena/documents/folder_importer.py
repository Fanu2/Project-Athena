"""
Folder document discovery.

This module discovers importable documents inside a folder without
performing any import or indexing operations.
"""

from __future__ import annotations

from pathlib import Path

from athena.documents.constants import SUPPORTED_DOCUMENT_TYPES


class FolderImporter:
    """
    Discover importable documents inside a folder.

    The importer only scans the filesystem and returns supported
    document paths. It does not perform any document import,
    indexing, embedding generation, or database operations.
    """

    def discover_documents(
        self,
        folder: Path,
    ) -> list[Path]:
        """
        Discover supported documents recursively.

        Parameters
        ----------
        folder:
            Root folder to scan.

        Returns
        -------
        list[Path]
            Sorted list of supported document paths.

        Raises
        ------
        FileNotFoundError
            If the folder does not exist.

        NotADirectoryError
            If the supplied path is not a directory.
        """

        if not folder.exists():
            raise FileNotFoundError(folder)

        if not folder.is_dir():
            raise NotADirectoryError(folder)

        documents = [
            path for path in folder.rglob("*") if path.is_file() and self._is_supported(path)
        ]

        return sorted(documents)

    def _is_supported(
        self,
        path: Path,
    ) -> bool:
        """
        Return True if the file extension is supported.
        """

        return path.suffix.lower() in SUPPORTED_DOCUMENT_TYPES
