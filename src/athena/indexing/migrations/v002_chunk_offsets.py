"""
Add chunk offset columns.
"""

from __future__ import annotations

import sqlite3

from athena.indexing.migrations.migration import (
    Migration,
)


class V002ChunkOffsets(Migration):
    """Add start/end offsets to the chunks table."""

    version = 2

    def apply(
        self,
        connection: sqlite3.Connection,
    ) -> None:
        """Apply the migration."""

        cursor = connection.execute(
            "PRAGMA table_info(chunks)"
        )

        columns = {
            row[1]
            for row in cursor.fetchall()
        }

        if "start_offset" not in columns:
            connection.execute(
                """
                ALTER TABLE chunks
                ADD COLUMN start_offset
                INTEGER NOT NULL
                DEFAULT 0
                """
            )

        if "end_offset" not in columns:
            connection.execute(
                """
                ALTER TABLE chunks
                ADD COLUMN end_offset
                INTEGER NOT NULL
                DEFAULT 0
                """
            )