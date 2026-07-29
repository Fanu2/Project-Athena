"""
Tests for conversation context enricher.
"""

from __future__ import annotations

from athena.ai.llm.conversation_context import (
    ConversationContext,
)
from athena.ai.llm.conversation_context_enricher import (
    ConversationContextEnricher,
)
from athena.ai.llm.memory_knowledge_context import (
    MemoryKnowledgeContext,
)


def test_enrich_context_with_knowledge() -> None:
    provider = MemoryKnowledgeContext(
        {
            "athena": [
                "Offline AI workstation",
                "Personal knowledge companion",
            ]
        }
    )

    context = ConversationContext(
        conversation_id="test",
    )

    enriched = (
        ConversationContextEnricher(
            provider
        )
        .enrich(
            context,
            "athena",
        )
    )

    assert enriched.retrieved_knowledge == [
        "Offline AI workstation",
        "Personal knowledge companion",
    ]


def test_enrich_empty_knowledge() -> None:
    provider = MemoryKnowledgeContext()

    context = ConversationContext(
        conversation_id="test",
    )

    enriched = (
        ConversationContextEnricher(
            provider
        )
        .enrich(
            context,
            "unknown",
        )
    )

    assert enriched.retrieved_knowledge == []
