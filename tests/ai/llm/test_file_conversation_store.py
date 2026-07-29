"""
Tests for file conversation store.
"""

from __future__ import annotations

from pathlib import Path

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.file_conversation_store import (
    FileConversationStore,
)
from athena.ai.llm.message import Message


def test_save_and_restore_conversation(
    tmp_path: Path,
) -> None:
    store = FileConversationStore(
        tmp_path
    )

    conversation = Conversation(
        title="Persistent Athena",
    )

    conversation.add_message(
        Message(
            role="user",
            content="Remember this",
        )
    )

    store.save(
        conversation
    )

    restored = store.get(
        conversation.conversation_id
    )

    assert restored.title == (
        "Persistent Athena"
    )

    assert restored.history()[0].content == (
        "Remember this"
    )


def test_file_exists_after_save(
    tmp_path: Path,
) -> None:
    store = FileConversationStore(
        tmp_path
    )

    conversation = Conversation()

    store.save(
        conversation
    )

    assert store.exists(
        conversation.conversation_id
    )


def test_delete_file_conversation(
    tmp_path: Path,
) -> None:
    store = FileConversationStore(
        tmp_path
    )

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


def test_list_file_conversations(
    tmp_path: Path,
) -> None:
    store = FileConversationStore(
        tmp_path
    )

    store.save(
        Conversation()
    )

    store.save(
        Conversation()
    )

    assert len(
        store.list_all()
    ) == 2
