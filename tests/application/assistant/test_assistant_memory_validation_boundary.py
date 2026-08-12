"""
Tests for assistant memory validation boundary.
"""

from datetime import datetime

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)

from athena.application.assistant.memory_quality import (
    AssistantMemoryQualityService,
)


def test_invalid_memory_missing_key():

    service = AssistantMemoryQualityService()

    memory = AssistantMemoryItem(
        key="",
        value="concise answers",
        source="user",
        scope="global",
        created_at=datetime.now(),
    )

    result = service.validate(
        memory,
    )

    assert result.valid is False

    assert (
        "missing_key"
        in result.warnings
    )


def test_invalid_memory_missing_value():

    service = AssistantMemoryQualityService()

    memory = AssistantMemoryItem(
        key="style",
        value="",
        source="user",
        scope="global",
        created_at=datetime.now(),
    )

    result = service.validate(
        memory,
    )

    assert result.valid is False

    assert (
        "missing_value"
        in result.warnings
    )
