"""
Embedding repository.

Stores vector embeddings in SQLite.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from athena.ai.embeddings.models import EmbeddingRecord


class EmbeddingRepository:
    """SQLite repository for embeddings."""

    def __init__(
        self,
        database_path: Path,
    ) -> None:
        """Initialize repository."""

        self._database_path = database_path

        self._initialize()

    def _initialize(self) -> None:
        """Create database table."""

        with sqlite3.connect(
            self._database_path,
        ) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS embeddings (
                    chunk_id TEXT PRIMARY KEY,
                    model_name TEXT NOT NULL,
                    vector TEXT NOT NULL,
                    created TEXT NOT NULL
                )
                """,
            )

    def save(
        self,
        embedding: EmbeddingRecord,
    ) -> None:
        """Save an embedding."""

        with sqlite3.connect(
            self._database_path,
        ) as connection:
            connection.execute(
                """
                INSERT OR REPLACE INTO embeddings
                (
                    chunk_id,
                    model_name,
                    vector,
                    created
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    embedding.chunk_id,
                    embedding.model_name,
                    json.dumps(
                        embedding.vector,
                    ),
                    embedding.created.isoformat(),
                ),
            )

    def get(
        self,
        chunk_id: str,
    ) -> EmbeddingRecord | None:
        """Retrieve embedding by chunk."""

        with sqlite3.connect(
            self._database_path,
        ) as connection:
            row = connection.execute(
                """
                SELECT
                    chunk_id,
                    model_name,
                    vector,
                    created
                FROM embeddings
                WHERE chunk_id = ?
                """,
                (chunk_id,),
            ).fetchone()

        if row is None:
            return None

        return EmbeddingRecord(
            chunk_id=row[0],
            model_name=row[1],
            vector=json.loads(
                row[2],
            ),
            created=datetime.fromisoformat(
                row[3],
            ),
        )

    def exists(
        self,
        chunk_id: str,
    ) -> bool:
        """Check if embedding exists."""

        return (
            self.get(
                chunk_id,
            )
            is not None
        )

    def delete(
        self,
        chunk_id: str,
    ) -> None:
        """Delete embedding."""

        with sqlite3.connect(
            self._database_path,
        ) as connection:
            connection.execute(
                """
                DELETE FROM embeddings
                WHERE chunk_id = ?
                """,
                (chunk_id,),
            )

    def list_all(self) -> list[EmbeddingRecord]:
        """Return all embeddings."""

        with sqlite3.connect(
            self._database_path,
        ) as connection:
            rows = connection.execute("""
                SELECT
                    chunk_id,
                    model_name,
                    vector,
                    created
                FROM embeddings
                """).fetchall()

        return [
            EmbeddingRecord(
                chunk_id=row[0],
                model_name=row[1],
                vector=json.loads(row[2]),
                created=datetime.fromisoformat(row[3]),
            )
            for row in rows
        ]
