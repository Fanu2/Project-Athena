"""
Tests for engine memory store integration.
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


def test_engine_reads_explicit_memory():

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

    memory = engine.load_memory(
        "style",
    )

    assert memory is not None

    assert (
        memory.value
        == "concise answers"
    )
