"""
Tests for conversation analyzer.
"""

from __future__ import annotations

from athena.ai.llm.conversation import Conversation
from athena.ai.llm.conversation_analyzer import (
    ConversationAnalyzer,
)
from athena.ai.llm.message import Message


def test_analyze_message_count() -> None:
    conversation = Conversation()

    conversation.add_message(
        Message(
            role="user",
            content="Explain RAG",
        )
    )

    conversation.add_message(
        Message(
            role="assistant",
            content="RAG uses retrieval.",
        )
    )

    metadata = ConversationAnalyzer().analyze(
        conversation
    )

    assert metadata.message_count == 2


def test_generate_title_when_missing() -> None:
    conversation = Conversation()

    conversation.add_message(
        Message(
            role="user",
            content="Explain Athena architecture",
        )
    )

    metadata = ConversationAnalyzer().analyze(
        conversation
    )

    assert metadata.title.startswith(
        "Explain Athena"
    )


def test_extract_topics() -> None:
    conversation = Conversation()

    conversation.add_message(
        Message(
            role="user",
            content="Athena uses Python with RAG and LLM models.",
        )
    )

    metadata = ConversationAnalyzer().analyze(
        conversation
    )

    assert "python" in metadata.topics
    assert "rag" in metadata.topics
    assert "llm" in metadata.topics
    assert "athena" in metadata.topics
