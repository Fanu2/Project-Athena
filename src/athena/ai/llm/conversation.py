"""
Conversation persistence model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from athena.ai.llm.message import Message


@dataclass(slots=True)
class Conversation:
    """Persistent conversation model."""

    title: str = ""

    conversation_id: str = field(
        default_factory=lambda: str(uuid4())
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    messages: list[Message] = field(
        default_factory=list
    )

    def add_message(
        self,
        message: Message,
    ) -> None:
        """Add message and update timestamp."""

        self.messages.append(message)

        self.updated_at = datetime.now(
            timezone.utc
        )

    def history(self) -> list[Message]:
        """Return conversation history."""

        return list(self.messages)
