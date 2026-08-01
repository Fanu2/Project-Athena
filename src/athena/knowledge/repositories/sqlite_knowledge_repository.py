"""
Athena SQLite Knowledge Repository

Persistent storage for KnowledgeObject.
"""

from __future__ import annotations

import json
import sqlite3
import threading

from uuid import UUID

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


class SQLiteKnowledgeRepository:
    """
    SQLite implementation of knowledge storage.

    Stores canonical Athena KnowledgeObjects.

    Thread-safe for background workers.
    """

    def __init__(
        self,
        database_path: str,
    ) -> None:

        self._database_path = database_path

        self._lock = threading.Lock()

        self._connection = sqlite3.connect(
            database_path,
            check_same_thread=False,
        )

        self._create_table()

    def _create_table(
        self,
    ) -> None:

        with self._lock:

            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS knowledge_objects (
                    object_id TEXT PRIMARY KEY,
                    object_type TEXT,
                    title TEXT,
                    content TEXT,
                    confidence REAL,
                    metadata TEXT
                )
                """
            )

            self._connection.commit()

    def save(
        self,
        knowledge_object: KnowledgeObject,
    ) -> None:
        """
        Persist a KnowledgeObject.
        """

        print(
            "KNOWLEDGE SAVE:",
            knowledge_object.title,
            "DB:",
            self._database_path,
        )

        with self._lock:

            self._connection.execute(
                """
                INSERT OR REPLACE INTO knowledge_objects
                (
                    object_id,
                    object_type,
                    title,
                    content,
                    confidence,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(
                        knowledge_object.object_id
                    ),
                    knowledge_object.object_type,
                    knowledge_object.title,
                    knowledge_object.content,
                    knowledge_object.confidence,
                    json.dumps(
                        knowledge_object.metadata
                    ),
                ),
            )

            self._connection.commit()

        print(
            "KNOWLEDGE SAVED:",
            knowledge_object.object_id,
        )

    def list_all(
        self,
    ) -> list[KnowledgeObject]:
        """
        Return all stored knowledge objects.
        """

        with self._lock:

            rows = (
                self._connection
                .execute(
                    """
                    SELECT
                        object_id,
                        object_type,
                        title,
                        content,
                        confidence,
                        metadata
                    FROM knowledge_objects
                    """
                )
                .fetchall()
            )

        return [
            self._row_to_object(row)
            for row in rows
        ]

    def get(
        self,
        object_id: UUID,
    ) -> KnowledgeObject | None:
        """
        Retrieve a knowledge object.
        """

        with self._lock:

            row = (
                self._connection
                .execute(
                    """
                    SELECT
                        object_id,
                        object_type,
                        title,
                        content,
                        confidence,
                        metadata
                    FROM knowledge_objects
                    WHERE object_id = ?
                    """,
                    (
                        str(object_id),
                    ),
                )
                .fetchone()
            )

        if row is None:
            return None

        return self._row_to_object(
            row
        )

    def find_by_type(
        self,
        object_type: str,
    ) -> list[KnowledgeObject]:
        """
        Find knowledge objects by type.
        """

        with self._lock:

            rows = (
                self._connection
                .execute(
                    """
                    SELECT
                        object_id,
                        object_type,
                        title,
                        content,
                        confidence,
                        metadata
                    FROM knowledge_objects
                    WHERE object_type = ?
                    """,
                    (
                        object_type,
                    ),
                )
                .fetchall()
            )

        return [
            self._row_to_object(row)
            for row in rows
        ]

    def _row_to_object(
        self,
        row,
    ) -> KnowledgeObject:
        """
        Convert SQLite row into domain object.
        """

        return KnowledgeObject(
            object_id=UUID(row[0]),
            object_type=row[1],
            title=row[2],
            content=row[3],
            confidence=row[4],
            metadata=(
                json.loads(row[5])
                if row[5]
                else {}
            ),
        )