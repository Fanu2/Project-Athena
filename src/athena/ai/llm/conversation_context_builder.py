"""
Conversation context builder.
"""

from __future__ import annotations

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_context import (
    ConversationContext,
)


class ConversationContextBuilder:
    """Build execution context from conversation."""

    def __init__(
        self,
        max_messages: int = 10,
    ) -> None:
        """Initialize builder."""

        self._max_messages = max_messages

    def build(
        self,
        conversation: Conversation,
    ) -> ConversationContext:
        """Build conversation context."""

        messages = conversation.history()

        recent = messages[
            -self._max_messages:
        ]

        return ConversationContext(
            conversation_id=(
                conversation.conversation_id
            ),
            recent_messages=[
                message.content
                for message in recent
            ],
            summary=(
                conversation.metadata.summary
                if conversation.metadata
                else ""
            ),
        )
