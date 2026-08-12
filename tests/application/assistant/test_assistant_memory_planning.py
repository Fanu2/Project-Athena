"""
Tests for memory-aware planning.
"""

from datetime import datetime

from athena.ai.intent.service import (
    IntentService,
)

from athena.application.assistant.engine import (
    AssistantEngine,
)

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)


def test_memory_appears_in_plan_context():

    engine = AssistantEngine(
        IntentService(),
    )

    engine.set_memories(
        (
            AssistantMemoryItem(
                key="style",
                value="concise answers",
                source="user",
                scope="global",
                created_at=datetime.now(),
            ),
        )
    )

    assert (
        len(engine._memories)
        == 1
    )
