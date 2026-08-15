"""
SQLite collection-document repository.

Manages documents inside collections.
"""

from __future__ import annotations

import sqlite3
from uuid import UUID


class SQLiteCollectionDocumentRepository:
    """
    SQLite-backed collection-document links.
    """

    def __init__(
        self,
        database_path,
    ) -> None:

        self._database_path = database_path

        self._database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

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
                CREATE TABLE IF NOT EXISTS collection_documents (
                    collection_id TEXT NOT NULL,
                    document_id TEXT NOT NULL,
                    PRIMARY KEY (
                        collection_id,
                        document_id
                    )
                )
                """
            )

    def add_document(
        self,
        collection_id: UUID,
        document_id: str,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                INSERT OR IGNORE INTO collection_documents (
                    collection_id,
                    document_id
                )
                VALUES (?, ?)
                """,
                (
                    str(collection_id),
                    document_id,
                ),
            )

    def remove_document(
        self,
        collection_id: UUID,
        document_id: str,
    ) -> None:

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM collection_documents
                WHERE collection_id = ?
                AND document_id = ?
                """,
                (
                    str(collection_id),
                    document_id,
                ),
            )

    def get_documents(
        self,
        collection_id: UUID,
    ) -> list[str]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT document_id
                FROM collection_documents
                WHERE collection_id = ?
                """,
                (
                    str(collection_id),
                ),
            ).fetchall()

        return [
            row[0]
            for row in rows
        ]

    def get_collections(
        self,
        document_id: str,
    ) -> list[UUID]:

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT collection_id
                FROM collection_documents
                WHERE document_id = ?
                """,
                (
                    document_id,
                ),
            ).fetchall()

        return [
            UUID(row[0])
            for row in rows
        ]