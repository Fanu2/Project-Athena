"""
Tests for assistant memory models.
"""

from datetime import datetime

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)


def test_memory_item_creation():

    item = AssistantMemoryItem(
        key="response_style",
        value="Prefer concise answers",
        source="user",
        scope="global",
        created_at=datetime.now(),
    )

    assert (
        item.key
        == "response_style"
    )

    assert (
        item.source
        == "user"
    )

    assert (
        item.scope
        == "global"
    )
