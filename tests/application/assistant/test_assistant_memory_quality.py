"""
Tests for assistant memory quality.
"""

from datetime import datetime

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)

from athena.application.assistant.memory_quality import (
    AssistantMemoryQualityService,
)


def test_memory_quality_validates_item():

    service = AssistantMemoryQualityService()

    memory = AssistantMemoryItem(
        key="style",
        value="concise answers",
        source="user",
        scope="global",
        created_at=datetime.now(),
    )

    result = service.validate(
        memory,
    )

    assert result.valid is True

    assert (
        "key_present"
        in result.checks
    )

    assert (
        "value_present"
        in result.checks
    )
