"""
Conversation runtime integration test.
"""

from __future__ import annotations

from unittest.mock import Mock

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_execution_service import (
    ConversationExecutionService,
)
from athena.ai.llm.conversation_context_enricher import (
    ConversationContextEnricher,
)
from athena.ai.llm.memory_knowledge_context import (
    MemoryKnowledgeContext,
)
from athena.ai.llm.models import LLMResponse
from athena.ai.llm.runtime_request import RuntimeRequest


def test_complete_conversation_runtime() -> None:
    executor = Mock()

    executor.execute.return_value = LLMResponse(
        text="Athena understands this conversation.",
        model="qwen3:4b",
    )

    knowledge = MemoryKnowledgeContext(
        {
            "athena": [
                "Athena is an offline AI assistant."
            ]
        }
    )

    service = ConversationExecutionService(
        enricher=ConversationContextEnricher(
            knowledge
        ),
        executor=executor,
    )

    conversation = Conversation()

    result = service.execute(
        conversation,
        "athena",
        RuntimeRequest(),
    )

    assert (
        result.response.text
        ==
        "Athena understands this conversation."
    )

    history = conversation.history()

    assert len(history) == 1

    assert history[0].role == "assistant"
