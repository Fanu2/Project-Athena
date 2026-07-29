"""
Tests for conversation serializer.
"""

from __future__ import annotations

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_serializer import (
    ConversationSerializer,
)
from athena.ai.llm.message import Message


def test_serialize_conversation() -> None:
    conversation = Conversation(
        title="Athena Research",
    )

    conversation.add_message(
        Message(
            role="user",
            content="Explain RAG",
        )
    )

    data = ConversationSerializer().to_dict(
        conversation
    )

    assert data["title"] == (
        "Athena Research"
    )

    assert len(
        data["messages"]
    ) == 1


def test_deserialize_conversation() -> None:
    serializer = ConversationSerializer()

    conversation = Conversation(
        title="Test",
    )

    conversation.add_message(
        Message(
            role="assistant",
            content="Answer",
        )
    )

    data = serializer.to_dict(
        conversation
    )

    restored = serializer.from_dict(
        data
    )

    assert restored.title == "Test"

    assert restored.history()[0].content == (
        "Answer"
    )


def test_preserve_conversation_id() -> None:
    serializer = ConversationSerializer()

    conversation = Conversation(
        title="Identity",
    )

    restored = serializer.from_dict(
        serializer.to_dict(
            conversation
        )
    )

    assert restored.conversation_id == (
        conversation.conversation_id
    )
