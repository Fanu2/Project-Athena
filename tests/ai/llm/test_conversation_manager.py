"""
Tests for ConversationManager.
"""

from __future__ import annotations

from athena.ai.llm.conversation_manager import (
    ConversationManager,
)
from athena.ai.llm.memory_conversation_store import (
    MemoryConversationStore,
)
from athena.ai.llm.message import Message


def test_create_conversation() -> None:
    store = MemoryConversationStore()

    manager = ConversationManager(
        store
    )

    conversation = manager.create(
        "Athena Research",
    )

    assert store.exists(
        conversation.conversation_id
    )

    assert conversation.title == (
        "Athena Research"
    )


def test_open_session_from_conversation() -> None:
    store = MemoryConversationStore()

    manager = ConversationManager(
        store
    )

    conversation = manager.create()

    conversation.add_message(
        Message(
            role="user",
            content="Hello Athena",
        )
    )

    store.save(
        conversation
    )

    session = manager.open_session(
        conversation.conversation_id
    )

    assert len(
        session.history()
    ) == 1

    assert session.history()[0].content == (
        "Hello Athena"
    )


def test_save_session_updates_conversation() -> None:
    store = MemoryConversationStore()

    manager = ConversationManager(
        store
    )

    conversation = manager.create()

    session = manager.open_session(
        conversation.conversation_id
    )

    session.add_message(
        Message(
            role="assistant",
            content="Welcome",
        )
    )

    manager.save_session(
        conversation,
        session,
    )

    restored = store.get(
        conversation.conversation_id
    )

    assert restored.history()[0].content == (
        "Welcome"
    )
