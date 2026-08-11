"""
Conversation item delegate.
"""

from __future__ import annotations

from PySide6.QtCore import (
    QRect,
    QModelIndex,
    QSize,
    Qt,
)

from PySide6.QtGui import (
    QFont,
    QPainter,
    QTextDocument,
)

from PySide6.QtWidgets import (
    QStyle,
    QStyleOptionViewItem,
    QStyledItemDelegate,
)


class ConversationDelegate(
    QStyledItemDelegate,
):
    """
    Delegate rendering Athena conversation cards.
    """

    SPEAKER_ROLE = (
        Qt.ItemDataRole.UserRole + 1
    )

    TEXT_ROLE = (
        Qt.ItemDataRole.UserRole + 2
    )


    def sizeHint(
        self,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> QSize:
        """
        Calculate dynamic message card height.
        """

        text = index.data(
            self.TEXT_ROLE,
        )

        if not text:
            return QSize(
                option.rect.width(),
                70,
            )

        document = QTextDocument()

        document.setPlainText(
            str(text),
        )

        document.setTextWidth(
            max(
                option.rect.width() - 60,
                300,
            ),
        )

        height = int(
            document.size().height(),
        )

        return QSize(
            option.rect.width(),
            height + 70,
        )


    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> None:
        """
        Draw conversation message card.
        """

        painter.save()

        speaker = index.data(
            self.SPEAKER_ROLE,
        )

        text = index.data(
            self.TEXT_ROLE,
        )


        #
        # Message identity
        #

        if speaker == "You":

            title = "👤 You"

            background = (
                option.palette
                .alternateBase()
            )

        elif speaker == "Athena":

            title = "🤖 Athena"

            background = (
                option.palette
                .base()
            )

        else:

            title = "⚙ System"

            background = (
                option.palette
                .midlight()
            )


        #
        # Selected message
        #

        if (
            option.state
            & QStyle.StateFlag.State_Selected
        ):
            background = (
                option.palette
                .highlight()
            )


        #
        # Card
        #

        rect = option.rect.adjusted(
            8,
            6,
            -8,
            -6,
        )

        painter.setBrush(
            background,
        )

        painter.setPen(
            Qt.PenStyle.NoPen,
        )

        painter.drawRoundedRect(
            rect,
            10,
            10,
        )


        #
        # Content area
        #

        content_rect = QRect(
            rect.left() + 14,
            rect.top() + 10,
            rect.width() - 28,
            rect.height() - 20,
        )


        #
        # Header
        #

        title_font = QFont()

        title_font.setBold(
            True,
        )

        title_font.setPointSize(
            title_font.pointSize() + 1,
        )

        painter.setFont(
            title_font,
        )

        painter.setPen(
            option.palette.text().color()),
        

        header_rect = QRect(
            content_rect.left(),
            content_rect.top(),
            content_rect.width(),
            24,
        )

        painter.drawText(
            header_rect,
            (
                Qt.AlignmentFlag.AlignLeft
                |
                Qt.AlignmentFlag.AlignVCenter
            ),
            title,
        )


        #
        # Rich text body
        #

        body_rect = QRect(
            content_rect.left(),
            content_rect.top() + 28,
            content_rect.width(),
            content_rect.height() - 28,
        )

        document = QTextDocument()

        document.setDefaultFont(
            QFont(),
        )

        document.setPlainText(
            str(text or ""),
        )

        document.setTextWidth(
            body_rect.width(),
        )

        painter.save()

        painter.translate(
            body_rect.topLeft(),
        )

        document.drawContents(
            painter,
        )

        painter.restore()


        painter.restore()