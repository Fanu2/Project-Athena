"""
In-memory conversation store.
"""

from __future__ import annotations

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_store import (
    ConversationStore,
)


class MemoryConversationStore(
    ConversationStore
):
    """Store conversations in memory."""

    def __init__(self) -> None:
        """Initialize store."""

        self._conversations: dict[
            str,
            Conversation,
        ] = {}

    def save(
        self,
        conversation: Conversation,
    ) -> None:
        """Save conversation."""

        self._conversations[
            conversation.conversation_id
        ] = conversation

    def get(
        self,
        conversation_id: str,
    ) -> Conversation:
        """Retrieve conversation."""

        return self._conversations[
            conversation_id
        ]

    def exists(
        self,
        conversation_id: str,
    ) -> bool:
        """Check conversation existence."""

        return (
            conversation_id
            in self._conversations
        )

    def delete(
        self,
        conversation_id: str,
    ) -> None:
        """Delete conversation."""

        del self._conversations[
            conversation_id
        ]

    def list_all(
        self,
    ) -> list[Conversation]:
        """List conversations."""

        return list(
            self._conversations.values()
        )
