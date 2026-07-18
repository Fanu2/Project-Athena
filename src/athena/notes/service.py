"""
Note service.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from athena.notes.models import Note
from athena.notes.storage import NoteStorage


class NoteService:
    """Manage research notes."""

    def __init__(
        self,
        storage_path: Path,
    ) -> None:
        """Initialize note service."""

        self._storage = NoteStorage(
            storage_path,
        )

        self._notes: dict[str, Note] = {}

        self._load()

    def _load(self) -> None:
        """Load notes from storage."""

        notes = self._storage.load()

        self._notes = {self._key(note.document_id): note for note in notes}

    def _save(self) -> None:
        """Save notes to storage."""

        self._storage.save(
            self.list_notes(),
        )

    def _key(
        self,
        document_id: str,
    ) -> str:
        """Create note key."""

        return document_id

    def create(
        self,
        document_id: str,
        content: str,
    ) -> None:
        """Create a note."""

        now = datetime.now()

        self._notes[self._key(document_id)] = Note(
            document_id=document_id,
            content=content,
            created=now,
            modified=now,
        )

        self._save()

    def update(
        self,
        document_id: str,
        content: str,
    ) -> None:
        """Update an existing note."""

        note = self._notes.get(
            self._key(document_id),
        )

        if note is None:
            return

        note.content = content
        note.modified = datetime.now()

        self._save()

    def delete(
        self,
        document_id: str,
    ) -> None:
        """Delete a note."""

        self._notes.pop(
            self._key(document_id),
            None,
        )

        self._save()

    def get(
        self,
        document_id: str,
    ) -> Note | None:
        """Return note for document."""

        return self._notes.get(
            self._key(document_id),
        )

    def list_notes(self) -> list[Note]:
        """Return all notes."""

        return list(
            self._notes.values(),
        )
