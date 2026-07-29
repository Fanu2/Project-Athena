from datetime import datetime
from pathlib import Path
import sqlite3
from uuid import UUID

from athena.knowledge.domain import (
    KnowledgeNote,
    KnowledgeNoteRepository,
)


class SQLiteKnowledgeNoteRepository(KnowledgeNoteRepository):

    def __init__(self, database_path: Path) -> None:
        self._connection = sqlite3.connect(database_path)
        self._create_table()

    def _create_table(self) -> None:
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS knowledge_notes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                markdown TEXT NOT NULL,
                archived INTEGER NOT NULL,
                favorite INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        self._connection.commit()

    def save(self, note: KnowledgeNote) -> None:
        self._connection.execute(
            """
            INSERT INTO knowledge_notes (
                id,
                title,
                markdown,
                archived,
                favorite,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                markdown = excluded.markdown,
                archived = excluded.archived,
                favorite = excluded.favorite,
                created_at = excluded.created_at,
                updated_at = excluded.updated_at
            """,
            (
                str(note.id),
                note.title,
                note.markdown,
                int(note.archived),
                int(note.favorite),
                note.created_at.isoformat(),
                note.updated_at.isoformat(),
            ),
        )
        self._connection.commit()

    def get(self, note_id: UUID) -> KnowledgeNote | None:

        cursor = self._connection.execute(
            """
            SELECT
                id,
                title,
                markdown,
                archived,
                favorite,
                created_at,
                updated_at
            FROM knowledge_notes
            WHERE id = ?
            """,
            (str(note_id),),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return KnowledgeNote(
            id=UUID(row[0]),
            title=row[1],
            markdown=row[2],
            archived=bool(row[3]),
            favorite=bool(row[4]),
            created_at=datetime.fromisoformat(row[5]),
            updated_at=datetime.fromisoformat(row[6]),
        )

    def delete(self, note_id: UUID) -> None:
        self._connection.execute(
            """
            DELETE FROM knowledge_notes
            WHERE id = ?
            """,
            (str(note_id),),
        )
        self._connection.commit()

    def list_all(self) -> list[KnowledgeNote]:

        cursor = self._connection.execute(
            """
            SELECT
                id,
                title,
                markdown,
                archived,
                favorite,
                created_at,
                updated_at
            FROM knowledge_notes
            ORDER BY created_at
            """
        )

        notes: list[KnowledgeNote] = []

        for row in cursor.fetchall():
            notes.append(
                KnowledgeNote(
                    id=UUID(row[0]),
                    title=row[1],
                    markdown=row[2],
                    archived=bool(row[3]),
                    favorite=bool(row[4]),
                    created_at=datetime.fromisoformat(row[5]),
                    updated_at=datetime.fromisoformat(row[6]),
                )
            )

        return notes
