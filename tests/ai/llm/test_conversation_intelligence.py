"""
Tests for conversation intelligence.
"""

from __future__ import annotations

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_intelligence import (
    ConversationIntelligence,
)
from athena.ai.llm.message import Message


def test_generate_conversation_insight() -> None:
    conversation = Conversation()

    conversation.add_message(
        Message(
            role="user",
            content="Explain Athena with RAG and Python.",
        )
    )

    insight = (
        ConversationIntelligence()
        .analyze(conversation)
    )

    assert insight.metadata.message_count == 1

    assert "rag" in (
        insight.metadata.topics
    )

    assert (
        "Explain Athena"
        in insight.summary.text
    )


def test_empty_conversation_insight() -> None:
    conversation = Conversation()

    insight = (
        ConversationIntelligence()
        .analyze(conversation)
    )

    assert (
        insight.metadata.message_count
        == 0
    )

    assert (
        insight.summary.text
        == "Empty conversation."
    )
