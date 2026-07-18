"""
Bookmark service.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from athena.bookmarks.models import Bookmark
from athena.bookmarks.storage import BookmarkStorage


class BookmarkService:
    """Manage document bookmarks."""

    def __init__(
        self,
        storage_path: Path,
    ) -> None:
        """Initialize bookmark service."""

        self._storage = BookmarkStorage(
            storage_path,
        )

        self._bookmarks: dict[str, Bookmark] = {}

        self._load()

    def _load(self) -> None:
        """Load bookmarks from storage."""

        bookmarks = self._storage.load()

        self._bookmarks = {bookmark.document_id: bookmark for bookmark in bookmarks}

    def _save(self) -> None:
        """Save bookmarks to storage."""

        self._storage.save(
            self.list_bookmarks(),
        )

    def add(
        self,
        document_id: str,
    ) -> None:
        """Add a bookmark."""

        self._bookmarks[document_id] = Bookmark(
            document_id=document_id,
            created=datetime.now(),
        )

        self._save()

    def remove(
        self,
        document_id: str,
    ) -> None:
        """Remove a bookmark."""

        self._bookmarks.pop(
            document_id,
            None,
        )

        self._save()

    def is_bookmarked(
        self,
        document_id: str,
    ) -> bool:
        """Check bookmark status."""

        return document_id in self._bookmarks

    def list_bookmarks(self) -> list[Bookmark]:
        """Return all bookmarks."""

        return list(
            self._bookmarks.values(),
        )
