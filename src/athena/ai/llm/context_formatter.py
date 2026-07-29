"""
Conversation context formatter.
"""

from __future__ import annotations

from athena.ai.llm.conversation_context import (
    ConversationContext,
)


class ContextFormatter:
    """Format conversation context for LLM."""

    def format(
        self,
        context: ConversationContext,
        prompt: str,
    ) -> str:
        """Create enriched prompt."""

        parts: list[str] = []

        if context.summary:
            parts.append(
                f"Conversation summary:\n{context.summary}"
            )

        if context.recent_messages:
            parts.append(
                "Recent messages:\n"
                + "\n".join(
                    context.recent_messages
                )
            )

        if context.retrieved_knowledge:
            parts.append(
                "Relevant knowledge:\n"
                + "\n".join(
                    context.retrieved_knowledge
                )
            )

        parts.append(
            f"User request:\n{prompt}"
        )

        return "\n\n".join(parts)
