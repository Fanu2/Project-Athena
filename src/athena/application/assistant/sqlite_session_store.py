"""
SQLite assistant session store.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from .session import (
    AssistantSession,
)

from .session_store import (
    AssistantSessionStore,
)


class SQLiteAssistantSessionStore(
    AssistantSessionStore,
):
    """
    SQLite-backed assistant session storage.
    """

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


    def _connect(
        self,
    ) -> sqlite3.Connection:
        """
        Return database connection.
        """

        return sqlite3.connect(
            self._database_path,
        )


    def _initialize_database(
        self,
    ) -> None:
        """
        Create session table.
        """

        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS assistant_sessions (
                    session_id TEXT PRIMARY KEY,
                    workspace_id TEXT NOT NULL,
                    workspace_name TEXT NOT NULL,
                    conversation_id TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )


    def save(
        self,
        session: AssistantSession,
    ) -> None:
        """
        Save or update session.
        """

        with self._connect() as connection:

            connection.execute(
                """
                INSERT OR REPLACE INTO assistant_sessions (
                    session_id,
                    workspace_id,
                    workspace_name,
                    conversation_id,
                    created_at,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    session.session_id,
                    session.workspace_id,
                    session.workspace_name,
                    session.conversation_id,
                    session.created_at.isoformat(),
                    session.updated_at.isoformat(),
                ),
            )


    def get(
        self,
        session_id: str,
    ) -> AssistantSession | None:
        """
        Retrieve session.
        """

        with self._connect() as connection:

            row = connection.execute(
                """
                SELECT
                    session_id,
                    workspace_id,
                    workspace_name,
                    conversation_id,
                    created_at,
                    updated_at
                FROM assistant_sessions
                WHERE session_id = ?
                """,
                (session_id,),
            ).fetchone()

        if row is None:
            return None

        return AssistantSession(
            session_id=row[0],
            workspace_id=row[1],
            workspace_name=row[2],
            conversation_id=row[3],
            created_at=datetime.fromisoformat(row[4]),
            updated_at=datetime.fromisoformat(row[5]),
        )


    def delete(
        self,
        session_id: str,
    ) -> None:
        """
        Delete session.
        """

        with self._connect() as connection:

            connection.execute(
                """
                DELETE FROM assistant_sessions
                WHERE session_id = ?
                """,
                (session_id,),
            )


    def list_sessions(
        self,
    ) -> tuple[
        AssistantSession,
        ...
    ]:
        """
        Return stored sessions.
        """

        with self._connect() as connection:

            rows = connection.execute(
                """
                SELECT
                    session_id,
                    workspace_id,
                    workspace_name,
                    conversation_id,
                    created_at,
                    updated_at
                FROM assistant_sessions
                ORDER BY updated_at DESC
                """
            ).fetchall()

        return tuple(
            AssistantSession(
                session_id=row[0],
                workspace_id=row[1],
                workspace_name=row[2],
                conversation_id=row[3],
                created_at=datetime.fromisoformat(row[4]),
                updated_at=datetime.fromisoformat(row[5]),
            )
            for row in rows
        )
