"""
Initial database schema.
"""

from __future__ import annotations

import sqlite3

from athena.indexing.migrations.migration import (
    Migration,
)


class V001Initial(Migration):
    """Create the initial database schema."""

    version = 1

    def apply(
        self,
        connection: sqlite3.Connection,
    ) -> None:
        """Apply the migration."""

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS chunks (
                chunk_id TEXT PRIMARY KEY,
                document_id TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                page_number INTEGER NOT NULL,
                text TEXT NOT NULL
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS
            idx_chunks_document
            ON chunks(document_id)
            """
        )