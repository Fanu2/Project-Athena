"""
RAG knowledge context adapter.
"""

from __future__ import annotations

from athena.ai.llm.knowledge_context import (
    KnowledgeContextProvider,
)
from athena.domain.ai.question import (
    Question,
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
        """Retrieve knowledge from Athena RAG."""

        results = self._retriever.retrieve(
            Question(
                text=query,
            )
        )

        return [
            getattr(
                result,
                "text",
                getattr(
                    result,
                    "content",
                    str(result),
                ),
            )
            for result in results
        ]