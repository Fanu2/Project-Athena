"""
Conversation item delegate.
"""

from __future__ import annotations

from PySide6.QtCore import (
    QModelIndex,
    QSize,
)
from PySide6.QtWidgets import (
    QStyleOptionViewItem,
    QStyledItemDelegate,
)


class ConversationDelegate(
    QStyledItemDelegate,
):
    """Delegate for rendering conversation messages."""

    def sizeHint(
        self,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> QSize:
        """Return the preferred size for a conversation item."""

        size = super().sizeHint(
            option,
            index,
        )

        size.setHeight(
            size.height() + 10,
        )

        return size
