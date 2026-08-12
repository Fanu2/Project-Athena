"""
Tests for engine memory quality boundary.
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

from athena.application.assistant.memory_quality import (
    AssistantMemoryQualityService,
)


def test_engine_can_validate_selected_memory():

    engine = AssistantEngine(
        IntentService(),
    )

    memory = AssistantMemoryItem(
        key="style",
        value="concise answers",
        source="user",
        scope="global",
        created_at=datetime.now(),
    )

    service = AssistantMemoryQualityService()

    result = service.validate(
        memory,
    )

    assert result.valid is True

    engine.set_memories(
        (
            memory,
        )
    )

    assert (
        len(engine._memories)
        == 1
    )
