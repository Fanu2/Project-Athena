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

import json
from pathlib import Path


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

    def save(
        self,
        path: Path,
    ) -> None:
        """Save the current conversation to a JSON file."""

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                self._to_dict(),
                file,
                indent=4,
                ensure_ascii=False,
            )

    def load(
        self,
        path: Path,
    ) -> None:
        """Load a conversation from a JSON file."""

        if not path.exists():
            self._conversation = Conversation()
            return

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        self._conversation = self._from_dict(
            data,
        )

    def _to_dict(
        self,
    ) -> dict:
        """Convert the conversation to a JSON-serializable dictionary."""

        return {
            "conversation_id": self._conversation.conversation_id,
            "title": self._conversation.title,
            "created": self._conversation.created.isoformat(),
            "modified": self._conversation.modified.isoformat(),
            "messages": [
                {
                    "role": message.role.value,
                    "text": message.text,
                    "timestamp": message.timestamp.isoformat(),
                }
                for message in self._conversation.messages
            ],
        }

    def _from_dict(
        self,
        data: dict,
    ) -> Conversation:
        """Create a conversation from a dictionary."""

        conversation = Conversation(
            conversation_id=data["conversation_id"],
            title=data["title"],
            created=datetime.fromisoformat(
                data["created"],
            ),
            modified=datetime.fromisoformat(
                data["modified"],
            ),
        )

        conversation.messages.extend(
            ConversationMessage(
                role=MessageRole(
                    message["role"],
                ),
                text=message["text"],
                timestamp=datetime.fromisoformat(
                    message["timestamp"],
                ),
            )
            for message in data.get(
                "messages",
                [],
            )
        )

        return conversation

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
