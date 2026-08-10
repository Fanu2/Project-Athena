"""
SQLite chunk repository.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from athena.indexing.migrations import MigrationManager
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

        return sqlite3.connect(
            self._database_path,
        )

    def _initialize_database(self) -> None:
        """Initialize or upgrade database schema."""

        with self._connect() as connection:
            MigrationManager(
                connection,
            ).upgrade()

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
                    document_path,
                    chunk_index,
                    page_number,
                    start_offset,
                    end_offset,
                    text
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        chunk.chunk_id,
                        chunk.document_id,
                        (
                            str(chunk.document_path)
                            if chunk.document_path
                            else None
                        ),
                        chunk.chunk_index,
                        chunk.page_number,
                        chunk.start_offset,
                        chunk.end_offset,
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
                    document_path,
                    chunk_index,
                    page_number,
                    start_offset,
                    end_offset,
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
                document_path=(
                    Path(row[2])
                    if row[2]
                    else None
                ),
                chunk_index=row[3],
                page_number=row[4],
                start_offset=row[5],
                end_offset=row[6],
                text=row[7],
            )
            for row in rows
        ]

    def get_chunk(
        self,
        chunk_id: str,
    ) -> DocumentChunk | None:
        """Return a single chunk by ID."""

        with self._connect() as connection:

            cursor = connection.execute(
                """
                SELECT
                    chunk_id,
                    document_id,
                    document_path,
                    chunk_index,
                    page_number,
                    start_offset,
                    end_offset,
                    text
                FROM chunks
                WHERE chunk_id = ?
                """,
                (chunk_id,),
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return DocumentChunk(
            chunk_id=row[0],
            document_id=row[1],
            document_path=(
                Path(row[2])
                if row[2]
                else None
            ),
            chunk_index=row[3],
            page_number=row[4],
            start_offset=row[5],
            end_offset=row[6],
            text=row[7],
        )

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
        Search indexed document chunks using token matching.
        """

        import re
        import unicodedata

        def normalize(
            value: str,
        ) -> str:

            value = unicodedata.normalize(
                "NFC",
                value,
            )

            value = value.lower()

            value = re.sub(
                r"[^\w\s\u0900-\u097F\u0980-\u09FF\u0A00-\u0A7F\u0F00-\u0FFF]",
                " ",
                value,
            )

            return value

        terms = [
            term
            for term in normalize(query).split()
            if len(term) > 1
        ]

        if not terms:
            return []

        conditions = " OR ".join(
            [
                "text LIKE ?"
                for _ in terms
            ]
        )

        parameters = [
            f"%{term}%"
            for term in terms
        ]

        parameters.append(limit)

        with self._connect() as connection:

            cursor = connection.execute(
                f"""
                SELECT
                    chunk_id,
                    document_id,
                    document_path,
                    chunk_index,
                    page_number,
                    start_offset,
                    end_offset,
                    text
                FROM chunks
                WHERE {conditions}
                ORDER BY chunk_index
                LIMIT ?
                """,
                parameters,
            )

            rows = cursor.fetchall()

        return [
            DocumentChunk(
                chunk_id=row[0],
                document_id=row[1],
                document_path=(
                    Path(row[2])
                    if row[2]
                    else None
                ),
                chunk_index=row[3],
                page_number=row[4],
                start_offset=row[5],
                end_offset=row[6],
                text=row[7],
            )
            for row in rows
        ]