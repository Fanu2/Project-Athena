"""
Bookmark storage.

Persists bookmarks inside workspace.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from athena.bookmarks.models import Bookmark


class BookmarkStorage:
    """JSON storage for bookmarks."""

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
        bookmarks: list[Bookmark],
    ) -> None:
        """Save bookmarks."""

        data = [
            {
                "document_id": bookmark.document_id,
                "created": bookmark.created.isoformat(),
            }
            for bookmark in bookmarks
        ]

        self._storage_path.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    def load(self) -> list[Bookmark]:
        """Load bookmarks."""

        if not self._storage_path.exists():
            return []

        data = json.loads(
            self._storage_path.read_text(
                encoding="utf-8",
            ),
        )

        return [
            Bookmark(
                document_id=item["document_id"],
                created=datetime.fromisoformat(
                    item["created"],
                ),
            )
            for item in data
        ]
