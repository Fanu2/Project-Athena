"""
Bookmark page.
"""

from __future__ import annotations

from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import (
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from athena.bookmarks.service import BookmarkService


class BookmarkPage(QWidget):
    """Displays bookmarked documents."""

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._bookmark_service: BookmarkService | None = None

        self.list_widget = QListWidget()

        self.remove_button = QPushButton(
            "Remove Bookmark",
        )

        self.remove_button.clicked.connect(
            self.remove_selected,
        )

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Create layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.list_widget,
        )

        layout.addWidget(
            self.remove_button,
        )

    def set_bookmark_service(
        self,
        service: BookmarkService,
    ) -> None:
        """Attach bookmark service."""

        self._bookmark_service = service

        self.refresh()

    def showEvent(
        self,
        event: QShowEvent,
    ) -> None:
        """Refresh bookmarks whenever page becomes visible."""

        self.refresh()

        super().showEvent(
            event,
        )

    def refresh(self) -> None:
        """Reload bookmarks."""

        self.list_widget.clear()

        if self._bookmark_service is None:
            return

        for bookmark in self._bookmark_service.list_bookmarks():
            self.list_widget.addItem(
                f"★ {bookmark.document_id}",
            )

    def remove_selected(self) -> None:
        """Remove selected bookmark."""

        if self._bookmark_service is None:
            return

        item = self.list_widget.currentItem()

        if item is None:
            return

        document_id = item.text().replace(
            "★ ",
            "",
        )

        self._bookmark_service.remove(
            document_id,
        )

        self.refresh()

    def clear(self) -> None:
        """Clear bookmark list."""

        self.list_widget.clear()
