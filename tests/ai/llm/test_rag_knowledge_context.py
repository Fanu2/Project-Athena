"""
Tests for RAG knowledge context adapter.
"""

from __future__ import annotations

from athena.ai.llm.rag_knowledge_context import (
    RAGKnowledgeContext,
)


class MockResult:
    def __init__(
        self,
        content: str,
    ) -> None:
        self.content = content


class MockRetriever:
    def retrieve(
        self,
        query: str,
    ) -> list[MockResult]:
        return [
            MockResult(
                "Athena RAG knowledge"
            ),
            MockResult(
                "Offline retrieval system"
            ),
        ]


def test_rag_adapter_retrieves_content() -> None:
    provider = RAGKnowledgeContext(
        MockRetriever()
    )

    result = provider.retrieve(
        "athena"
    )

    assert result == [
        "Athena RAG knowledge",
        "Offline retrieval system",
    ]


def test_rag_adapter_empty_results() -> None:
    class EmptyRetriever:
        def retrieve(
            self,
            query: str,
        ) -> list:
            return []

    provider = RAGKnowledgeContext(
        EmptyRetriever()
    )

    assert provider.retrieve(
        "unknown"
    ) == []
