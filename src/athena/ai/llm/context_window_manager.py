"""
Context window management.
"""

from __future__ import annotations

from athena.ai.llm.conversation_context import (
    ConversationContext,
)


class ContextWindowManager:
    """Control conversation context size."""

    def __init__(
        self,
        max_messages: int = 10,
        max_knowledge_items: int = 5,
    ) -> None:
        """Initialize limits."""

        self._max_messages = max_messages

        self._max_knowledge_items = (
            max_knowledge_items
        )

    def optimize(
        self,
        context: ConversationContext,
    ) -> ConversationContext:
        """Trim context to configured limits."""

        context.recent_messages = (
            context.recent_messages[
                -self._max_messages:
            ]
        )

        context.retrieved_knowledge = (
            context.retrieved_knowledge[
                :self._max_knowledge_items
            ]
        )

        return context
