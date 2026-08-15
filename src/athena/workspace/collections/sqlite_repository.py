"""
SQLite collection repository.

Stores workspace collections.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from uuid import UUID

from athena.domain.collection import Collection

from athena.repositories.collection_repository import (
    CollectionRepository,
)


class SQLiteCollectionRepository(CollectionRepository):
    """
    SQLite-backed collection repository.
    """

    def __init__(
        self,
        database_path,
    ) -> None:

        self._database_path = database_path

        self._initialize_database()

    def _connect(
        self,
    ) -> sqlite3.Connection:

        return sqlite3.connect(
            self._database_path,
        )

    def _initialize_database(
        self,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS collections (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def add(
        self,
        collection: Collection,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                INSERT INTO collections (
                    id,
                    name,
                    description,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    str(collection.id),
                    collection.name,
                    collection.description,
                    collection.created_at.isoformat(),
                    collection.updated_at.isoformat(),
                ),
            )

    def get(
        self,
        collection_id: UUID,
    ) -> Collection | None:

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT
                    id,
                    name,
                    description,
                    created_at,
                    updated_at
                FROM collections
                WHERE id = ?
                """,
                (
                    str(collection_id),
                ),
            ).fetchone()

        if row is None:
            return None

        return self._to_domain(
            row,
        )

    def get_all(
        self,
    ) -> list[Collection]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT
                    id,
                    name,
                    description,
                    created_at,
                    updated_at
                FROM collections
                ORDER BY name
                """
            ).fetchall()

        return [
            self._to_domain(row)
            for row in rows
        ]

    def update(
        self,
        collection: Collection,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                UPDATE collections
                SET
                    name = ?,
                    description = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    collection.name,
                    collection.description,
                    collection.updated_at.isoformat(),
                    str(collection.id),
                ),
            )

    def delete(
        self,
        collection_id: UUID,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM collections
                WHERE id = ?
                """,
                (
                    str(collection_id),
                ),
            )

    @staticmethod
    def _to_domain(
        row,
    ) -> Collection:

        return Collection(
            id=UUID(row[0]),
            name=row[1],
            description=row[2],
            created_at=datetime.fromisoformat(
                row[3],
            ),
            updated_at=datetime.fromisoformat(
                row[4],
            ),
        )
