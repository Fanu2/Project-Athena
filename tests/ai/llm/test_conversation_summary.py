"""
Tests for conversation summary.
"""

from __future__ import annotations

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_summary import (
    ConversationSummaryService,
)
from athena.ai.llm.message import Message


def test_empty_conversation_summary() -> None:
    conversation = Conversation()

    summary = (
        ConversationSummaryService()
        .summarize(conversation)
    )

    assert summary.text == (
        "Empty conversation."
    )

    assert summary.generated is False


def test_conversation_summary_content() -> None:
    conversation = Conversation()

    conversation.add_message(
        Message(
            role="user",
            content="Explain Athena architecture",
        )
    )

    summary = (
        ConversationSummaryService()
        .summarize(conversation)
    )

    assert (
        "Explain Athena architecture"
        in summary.text
    )

    assert summary.generated is False
