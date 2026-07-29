"""
Conversation summary service.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.ai.llm.conversation import Conversation


@dataclass(slots=True)
class ConversationSummary:
    """Conversation summary result."""

    text: str = ""

    generated: bool = False


class ConversationSummaryService:
    """Generate conversation summaries."""

    def summarize(
        self,
        conversation: Conversation,
    ) -> ConversationSummary:
        """Create summary."""

        messages = conversation.history()

        if not messages:
            return ConversationSummary(
                text="Empty conversation.",
                generated=False,
            )

        first = messages[0].content

        return ConversationSummary(
            text=(
                f"Conversation started with: "
                f"{first[:100]}"
            ),
            generated=False,
        )
