"""
Tests for explicit memory injection.
"""

from datetime import datetime

from athena.ai.intent.service import (
    IntentService,
)

from athena.application.assistant.engine import (
    AssistantEngine,
)

from athena.application.assistant.in_memory_store import (
    InMemoryAssistantMemoryStore,
)

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)


def test_engine_loads_selected_memories():

    store = InMemoryAssistantMemoryStore()

    store.save(
        AssistantMemoryItem(
            key="style",
            value="concise answers",
            source="user",
            scope="global",
            created_at=datetime.now(),
        )
    )

    engine = AssistantEngine(
        IntentService(),
    )

    engine.set_memory_store(
        store,
    )

    memories = engine.load_memories(
        (
            "style",
        )
    )

    assert len(memories) == 1

    assert (
        memories[0].key
        == "style"
    )
