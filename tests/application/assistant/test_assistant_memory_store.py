"""
Tests for assistant memory store.
"""

from datetime import datetime

from athena.application.assistant.in_memory_store import (
    InMemoryAssistantMemoryStore,
)

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)


def test_memory_store_save_retrieve_delete():

    store = InMemoryAssistantMemoryStore()

    item = AssistantMemoryItem(
        key="style",
        value="concise",
        source="user",
        scope="global",
        created_at=datetime.now(),
    )

    store.save(
        item,
    )

    result = store.retrieve(
        "style",
    )

    assert result == item

    store.delete(
        "style",
    )

    assert (
        store.retrieve("style")
        is None
    )
