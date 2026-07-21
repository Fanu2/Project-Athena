"""
Conversation service.
"""

from __future__ import annotations

from datetime import datetime

from athena.conversation.models import (
    Conversation,
    ConversationMessage,
    MessageRole,
)


class ConversationService:
    """Manages the active conversation."""

    def __init__(self) -> None:
        self._conversation = Conversation()

    def new_conversation(
        self,
        title: str = "New Conversation",
    ) -> Conversation:
        """Create a new conversation."""

        self._conversation = Conversation(
            title=title,
        )

        return self._conversation

    @property
    def conversation(self) -> Conversation:
        """Return the current conversation."""

        return self._conversation

    def add_user_message(
        self,
        text: str,
    ) -> None:
        """Add a user message."""

        self._add_message(
            MessageRole.USER,
            text,
        )

    def add_assistant_message(
        self,
        text: str,
    ) -> None:
        """Add an assistant message."""

        self._add_message(
            MessageRole.ASSISTANT,
            text,
        )

    def add_system_message(
        self,
        text: str,
    ) -> None:
        """Add a system message."""

        self._add_message(
            MessageRole.SYSTEM,
            text,
        )

    def clear(self) -> None:
        """Clear the current conversation."""

        title = self._conversation.title

        self._conversation = Conversation(
            title=title,
        )

    def _add_message(
        self,
        role: MessageRole,
        text: str,
    ) -> None:
        """Append a message to the conversation."""

        message = ConversationMessage(
            role=role,
            text=text,
        )

        self._conversation.messages.append(
            message,
        )

        self._conversation.modified = datetime.now()
