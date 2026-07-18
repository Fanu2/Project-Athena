"""
SQLite chunk repository.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from athena.indexing.models import DocumentChunk
from athena.indexing.repositories.base import ChunkRepository


class SQLiteChunkRepository(ChunkRepository):
    """SQLite-backed repository."""

    def __init__(
        self,
        database_path: Path,
    ) -> None:
        """Initialize the repository."""

        self._database_path = database_path

        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        """Return a database connection."""

        return sqlite3.connect(self._database_path)

    def _initialize_database(self) -> None:
        """Create database schema."""

        with self._connect() as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    chunk_id TEXT PRIMARY KEY,
                    document_id TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    page_number INTEGER NOT NULL,
                    text TEXT NOT NULL
                )
                """)

            connection.execute("""
                CREATE INDEX IF NOT EXISTS
                idx_chunks_document
                ON chunks(document_id)
                """)

    def save_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        """Save document chunks."""

        if not chunks:
            return

        document_id = chunks[0].document_id

        with self._connect() as connection:
            connection.execute(
                "DELETE FROM chunks WHERE document_id = ?",
                (document_id,),
            )

            connection.executemany(
                """
                INSERT INTO chunks (
                    chunk_id,
                    document_id,
                    chunk_index,
                    page_number,
                    text
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        chunk.chunk_id,
                        chunk.document_id,
                        chunk.chunk_index,
                        chunk.page_number,
                        chunk.text,
                    )
                    for chunk in chunks
                ],
            )

    def load_chunks(
        self,
        document_id: str,
    ) -> list[DocumentChunk]:
        """Load document chunks."""

        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    chunk_id,
                    document_id,
                    chunk_index,
                    page_number,
                    text
                FROM chunks
                WHERE document_id = ?
                ORDER BY chunk_index
                """,
                (document_id,),
            )

            rows = cursor.fetchall()

        return [
            DocumentChunk(
                chunk_id=row[0],
                document_id=row[1],
                chunk_index=row[2],
                page_number=row[3],
                text=row[4],
            )
            for row in rows
        ]

    def delete_chunks(
        self,
        document_id: str,
    ) -> None:
        """Delete document chunks."""

        with self._connect() as connection:
            connection.execute(
                """
                DELETE FROM chunks
                WHERE document_id = ?
                """,
                (document_id,),
            )

    def search_chunks(
        self,
        query: str,
        limit: int = 20,
    ) -> list[DocumentChunk]:
        """
        Search indexed document chunks.

        Parameters
        ----------
        query:
            Search text.

        limit:
            Maximum number of results.

        Returns
        -------
        list[DocumentChunk]
            Matching document chunks.
        """

        with self._connect() as connection:
            cursor = connection.execute(
                """
                SELECT
                    chunk_id,
                    document_id,
                    chunk_index,
                    page_number,
                    text
                FROM chunks
                WHERE text LIKE ?
                ORDER BY document_id, chunk_index
                LIMIT ?
                """,
                (f"%{query}%", limit),
            )

            rows = cursor.fetchall()

        return [
            DocumentChunk(
                chunk_id=row[0],
                document_id=row[1],
                chunk_index=row[2],
                page_number=row[3],
                text=row[4],
            )
            for row in rows
        ]
