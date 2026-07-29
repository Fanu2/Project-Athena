"""
Conversation analyzer.
"""

from __future__ import annotations

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_metadata import (
    ConversationMetadata,
)


class ConversationAnalyzer:
    """Analyze conversation information."""

    def analyze(
        self,
        conversation: Conversation,
    ) -> ConversationMetadata:
        """Extract conversation metadata."""

        messages = conversation.history()

        title = (
            conversation.title
            if conversation.title
            else self._generate_title(
                messages
            )
        )

        topics = self._extract_topics(
            messages
        )

        return ConversationMetadata(
            title=title,
            message_count=len(messages),
            topics=topics,
        )

    def _generate_title(
        self,
        messages,
    ) -> str:
        """Generate basic title."""

        if not messages:
            return "Empty Conversation"

        content = messages[0].content

        return content[:40]

    def _extract_topics(
        self,
        messages,
    ) -> list[str]:
        """Extract simple keyword topics."""

        topics: list[str] = []

        keywords = [
            "python",
            "rag",
            "llm",
            "ai",
            "athena",
        ]

        text = " ".join(
            message.content.lower()
            for message in messages
        )

        for keyword in keywords:
            if keyword in text:
                topics.append(
                    keyword
                )

        return topics
