"""
SQLite document repository.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from athena.indexing.models import IndexedDocument
from athena.indexing.repositories.document_base import DocumentRepository


class SQLiteDocumentRepository(DocumentRepository):
    """SQLite-backed repository for indexed document metadata."""

    def __init__(
        self,
        database_path: Path,
    ) -> None:
        self._database_path = database_path

        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._database_path)

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    document_id TEXT PRIMARY KEY,
                    path TEXT NOT NULL,
                    title TEXT NOT NULL,
                    sha256 TEXT NOT NULL UNIQUE,
                    page_count INTEGER NOT NULL,
                    indexed_at TEXT NOT NULL
                )
                """)

    def save_document(
        self,
        document: IndexedDocument,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO documents (
                    document_id,
                    path,
                    title,
                    sha256,
                    page_count,
                    indexed_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    document.document_id,
                    str(document.path),
                    document.title,
                    document.sha256,
                    document.page_count,
                    document.indexed_at.isoformat(),
                ),
            )

    def load_document(
        self,
        document_id: str,
    ) -> IndexedDocument | None:
        raise NotImplementedError

    def exists_by_hash(
        self,
        sha256: str,
    ) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT 1
                FROM documents
                WHERE sha256 = ?
                LIMIT 1
                """,
                (sha256,),
            )

            return cursor.fetchone() is not None

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                DELETE FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            )
