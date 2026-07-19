"""
SQLite document repository.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
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
        return sqlite3.connect(
            self._database_path,
        )

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
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT
                    document_id,
                    path,
                    title,
                    sha256,
                    page_count,
                    indexed_at
                FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            ).fetchone()

        if row is None:
            return None

        return IndexedDocument(
            document_id=row[0],
            path=Path(row[1]),
            title=row[2],
            sha256=row[3],
            page_count=row[4],
            indexed_at=datetime.fromisoformat(row[5]),
        )

    def list_documents(
        self,
    ) -> list[IndexedDocument]:
        """Return all indexed documents."""

        with self._connect() as connection:
            rows = connection.execute("""
                SELECT
                    document_id,
                    path,
                    title,
                    sha256,
                    page_count,
                    indexed_at
                FROM documents
                ORDER BY title
                """).fetchall()

        return [
            IndexedDocument(
                document_id=row[0],
                path=Path(row[1]),
                title=row[2],
                sha256=row[3],
                page_count=row[4],
                indexed_at=datetime.fromisoformat(row[5]),
            )
            for row in rows
        ]

    def find_by_title(
        self,
        title: str,
    ) -> list[IndexedDocument]:
        """Find documents whose title contains the given text."""

        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    document_id,
                    path,
                    title,
                    sha256,
                    page_count,
                    indexed_at
                FROM documents
                WHERE title LIKE ?
                ORDER BY title
                """,
                (f"%{title}%",),
            ).fetchall()

        return [
            IndexedDocument(
                document_id=row[0],
                path=Path(row[1]),
                title=row[2],
                sha256=row[3],
                page_count=row[4],
                indexed_at=datetime.fromisoformat(row[5]),
            )
            for row in rows
        ]

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
