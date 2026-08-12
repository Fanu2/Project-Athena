"""
Tests for assistant memory context.
"""

from datetime import datetime

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)

from athena.application.assistant.context import (
    AssistantContext,
)


def test_context_accepts_explicit_memories():

    memory = AssistantMemoryItem(
        key="style",
        value="concise answers",
        source="user",
        scope="global",
        created_at=datetime.now(),
    )

    context = AssistantContext(
        intent=None,
        workspace=None,
        memories=(
            memory,
        ),
    )

    assert (
        context.memories[0].key
        == "style"
    )
