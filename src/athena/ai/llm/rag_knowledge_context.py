"""
RAG knowledge context adapter.
"""

from __future__ import annotations

from athena.ai.llm.knowledge_context import (
    KnowledgeContextProvider,
)


class RAGKnowledgeContext(
    KnowledgeContextProvider
):
    """Adapter for Athena retrieval system."""

    def __init__(
        self,
        retriever,
    ) -> None:
        """Initialize adapter."""

        self._retriever = retriever

    def retrieve(
        self,
        query: str,
    ) -> list[str]:
        """Retrieve knowledge from RAG."""

        results = self._retriever.retrieve(
            query
        )

        return [
            result.content
            for result in results
        ]
