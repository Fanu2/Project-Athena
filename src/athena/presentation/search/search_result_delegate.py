"""
Search result delegate.

Provides visual highlighting of search terms.
"""

from __future__ import annotations

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import (
    QPainter,
    QTextDocument,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QStyleOptionViewItem,
    QStyledItemDelegate,
)


class SearchResultDelegate(QStyledItemDelegate):
    """Custom delegate for search result rendering."""

    def __init__(
        self,
        parent: QAbstractItemView | None = None,
    ) -> None:
        super().__init__(parent)

        self._query = ""

    def set_query(
        self,
        query: str,
    ) -> None:
        """Set search query for highlighting."""

        self._query = query.strip()

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index,
    ) -> None:
        """Paint search result."""

        text = index.data(
            Qt.ItemDataRole.DisplayRole,
        )

        if not isinstance(text, str):
            return

        painter.save()

        document = QTextDocument()

        html = text.replace(
            "\n",
            "<br>",
        )

        if self._query:
            html = html.replace(
                self._query,
                f"<b>{self._query}</b>",
            )

        document.setHtml(
            html,
        )

        painter.translate(
            option.rect.topLeft(),
        )

        document.drawContents(
            painter,
            QRect(
                0,
                0,
                option.rect.width(),
                option.rect.height(),
            ),
        )

        painter.restore()
