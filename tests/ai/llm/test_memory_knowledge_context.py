"""
Tests for memory knowledge context.
"""

from __future__ import annotations

from athena.ai.llm.memory_knowledge_context import (
    MemoryKnowledgeContext,
)


def test_retrieve_existing_knowledge() -> None:
    provider = MemoryKnowledgeContext(
        {
            "athena": [
                "Offline AI workstation",
                "Personal knowledge companion",
            ]
        }
    )

    result = provider.retrieve(
        "athena"
    )

    assert result == [
        "Offline AI workstation",
        "Personal knowledge companion",
    ]


def test_retrieve_missing_knowledge() -> None:
    provider = MemoryKnowledgeContext()

    result = provider.retrieve(
        "unknown"
    )

    assert result == []
