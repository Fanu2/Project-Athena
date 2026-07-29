"""
Conversation context enricher.
"""

from __future__ import annotations

from athena.ai.llm.conversation_context import (
    ConversationContext,
)
from athena.ai.llm.knowledge_context import (
    KnowledgeContextProvider,
)


class ConversationContextEnricher:
    """Add knowledge to conversation context."""

    def __init__(
        self,
        provider: KnowledgeContextProvider,
    ) -> None:
        """Initialize enricher."""

        self._provider = provider

    def enrich(
        self,
        context: ConversationContext,
        query: str,
    ) -> ConversationContext:
        """Attach retrieved knowledge."""

        context.retrieved_knowledge = (
            self._provider.retrieve(
                query
            )
        )

        return context
