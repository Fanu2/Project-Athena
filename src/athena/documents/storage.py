"""
Document storage.
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from athena.documents.models import Document


class DocumentStorage:
    """Filesystem operations for workspace documents."""

    @staticmethod
    def copy_document(
        source: Path,
        documents_dir: Path,
    ) -> Path:
        """
        Copy a document into the workspace.

        Returns:
            Destination path.
        """

        documents_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = documents_dir / source.name

        shutil.copy2(
            source,
            destination,
        )

        return destination

    @staticmethod
    def remove_document(
        document: Path,
    ) -> None:
        """Delete a document."""

        document.unlink()

    @staticmethod
    def list_documents(
        documents_dir: Path,
    ) -> list[Document]:
        """Return all documents in the workspace."""

        if not documents_dir.exists():
            return []

        documents: list[Document] = []

        for path in sorted(documents_dir.iterdir()):

            if not path.is_file():
                continue

            stat = path.stat()

            documents.append(
                Document(
                    id=path.name,
                    name=path.name,
                    path=path,
                    size=stat.st_size,
                    created=datetime.fromtimestamp(stat.st_ctime),
                    modified=datetime.fromtimestamp(stat.st_mtime),
                )
            )

        return documents
