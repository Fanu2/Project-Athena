"""
Tests for conversation stores.
"""

from __future__ import annotations

import pytest

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.memory_conversation_store import (
    MemoryConversationStore,
)
from athena.ai.llm.message import Message


def test_save_and_get_conversation() -> None:
    store = MemoryConversationStore()

    conversation = Conversation(
        title="Athena Test",
    )

    store.save(
        conversation
    )

    loaded = store.get(
        conversation.conversation_id
    )

    assert loaded.title == (
        "Athena Test"
    )


def test_conversation_exists() -> None:
    store = MemoryConversationStore()

    conversation = Conversation()

    store.save(
        conversation
    )

    assert store.exists(
        conversation.conversation_id
    )


def test_delete_conversation() -> None:
    store = MemoryConversationStore()

    conversation = Conversation()

    store.save(
        conversation
    )

    store.delete(
        conversation.conversation_id
    )

    assert not store.exists(
        conversation.conversation_id
    )


def test_list_conversations() -> None:
    store = MemoryConversationStore()

    store.save(
        Conversation()
    )

    store.save(
        Conversation()
    )

    assert len(
        store.list_all()
    ) == 2


def test_conversation_messages_persist() -> None:
    store = MemoryConversationStore()

    conversation = Conversation()

    conversation.add_message(
        Message(
            role="user",
            content="Hello Athena",
        )
    )

    store.save(
        conversation
    )

    loaded = store.get(
        conversation.conversation_id
    )

    assert len(
        loaded.history()
    ) == 1

    assert loaded.history()[0].content == (
        "Hello Athena"
    )
