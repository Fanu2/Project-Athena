"""
Database migration manager.
"""

from __future__ import annotations

import sqlite3

from athena.indexing.migrations.v001_initial import (
    V001Initial,
)
from athena.indexing.migrations.v002_chunk_offsets import (
    V002ChunkOffsets,
)


class MigrationManager:
    """Manage database schema upgrades."""

    def __init__(
        self,
        connection: sqlite3.Connection,
    ) -> None:
        """Initialize the migration manager."""

        self._connection = connection

        self._migrations = (
            V001Initial(),
            V002ChunkOffsets(),
        )

    def upgrade(self) -> None:
        """Upgrade the database schema to the latest version."""

        current_version = self._schema_version()

        for migration in self._migrations:

            if migration.version <= current_version:
                continue

            migration.apply(
                self._connection,
            )

            self._connection.execute(
                f"PRAGMA user_version = {migration.version}"
            )

            self._connection.commit()

    def _schema_version(
        self,
    ) -> int:
        """Return the current database schema version."""

        cursor = self._connection.execute(
            "PRAGMA user_version"
        )

        row = cursor.fetchone()

        if row is None:
            return 0

        return int(row[0])