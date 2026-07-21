"""
Conversation list model.
"""

from __future__ import annotations

from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Qt,
)

from athena.conversation.models import (
    ConversationMessage,
    MessageRole,
)
from athena.conversation.service import (
    ConversationService,
)


class ConversationModel(QAbstractListModel):
    """Qt model exposing the current conversation."""

    SpeakerRole = Qt.ItemDataRole.UserRole + 1
    TextRole = Qt.ItemDataRole.UserRole + 2

    def __init__(
        self,
        conversation_service: ConversationService,
    ) -> None:
        """Initialize the conversation model."""
        super().__init__()

        self._conversation_service = conversation_service

    def rowCount(
        self,
        parent: QModelIndex = QModelIndex(),
    ) -> int:
        """Return the number of conversation messages."""

        if parent.isValid():
            return 0

        return len(
            self._conversation_service.conversation.messages,
        )

    def data(
        self,
        index: QModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | ConversationMessage | None:
        """Return data for a conversation message."""

        messages = self._conversation_service.conversation.messages

        if not index.isValid() or index.row() < 0 or index.row() >= len(messages):
            return None

        message = messages[index.row()]

        if role == Qt.ItemDataRole.DisplayRole:

            if message.role == MessageRole.USER:
                prefix = "You"

            elif message.role == MessageRole.ASSISTANT:
                prefix = "Athena"

            else:
                prefix = "System"

            return f"{prefix}:\n" f"{message.text}"

        if role == Qt.ItemDataRole.UserRole:
            return message

        if role == self.SpeakerRole:

            if message.role == MessageRole.USER:
                return "You"

            if message.role == MessageRole.ASSISTANT:
                return "Athena"

            return "System"

        if role == self.TextRole:
            return message.text

        return None

    def last_message(
        self,
    ) -> ConversationMessage | None:
        """Return the most recent conversation message."""

        messages = self._conversation_service.conversation.messages

        if not messages:
            return None

        return messages[-1]

    def refresh(
        self,
    ) -> None:
        """Notify Qt that the conversation has changed."""

        self.beginResetModel()
        self.endResetModel()
