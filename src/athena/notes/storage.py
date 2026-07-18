"""
Note storage.

Persists research notes inside workspace.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from athena.notes.models import Note


class NoteStorage:
    """JSON storage for research notes."""

    def __init__(
        self,
        storage_path: Path,
    ) -> None:
        """Initialize storage."""

        self._storage_path = storage_path

        self._storage_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        notes: list[Note],
    ) -> None:
        """Save notes."""

        data = [
            {
                "document_id": note.document_id,
                "content": note.content,
                "created": note.created.isoformat(),
                "modified": note.modified.isoformat(),
            }
            for note in notes
        ]

        self._storage_path.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    def load(self) -> list[Note]:
        """Load notes."""

        if not self._storage_path.exists():
            return []

        data = json.loads(
            self._storage_path.read_text(
                encoding="utf-8",
            ),
        )

        return [
            Note(
                document_id=item["document_id"],
                content=item["content"],
                created=datetime.fromisoformat(
                    item["created"],
                ),
                modified=datetime.fromisoformat(
                    item["modified"],
                ),
            )
            for item in data
        ]
