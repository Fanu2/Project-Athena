"""
Tests for conversation context builder.
"""

from __future__ import annotations

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_context_builder import (
    ConversationContextBuilder,
)
from athena.ai.llm.conversation_metadata import (
    ConversationMetadata,
)
from athena.ai.llm.message import Message


def test_build_context_with_messages() -> None:
    conversation = Conversation()

    conversation.add_message(
        Message(
            role="user",
            content="Explain Athena",
        )
    )

    context = (
        ConversationContextBuilder()
        .build(conversation)
    )

    assert context.conversation_id == (
        conversation.conversation_id
    )

    assert context.recent_messages == [
        "Explain Athena"
    ]


def test_build_context_with_summary() -> None:
    conversation = Conversation()

    conversation.metadata = ConversationMetadata(
        summary="Previous RAG discussion",
    )

    context = (
        ConversationContextBuilder()
        .build(conversation)
    )

    assert context.summary == (
        "Previous RAG discussion"
    )


def test_context_message_limit() -> None:
    conversation = Conversation()

    for index in range(5):
        conversation.add_message(
            Message(
                role="user",
                content=f"Message {index}",
            )
        )

    context = (
        ConversationContextBuilder(
            max_messages=2
        )
        .build(conversation)
    )

    assert context.recent_messages == [
        "Message 3",
        "Message 4",
    ]
