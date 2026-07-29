"""
In-memory knowledge context provider.
"""

from __future__ import annotations

from athena.ai.llm.knowledge_context import (
    KnowledgeContextProvider,
)


class MemoryKnowledgeContext(
    KnowledgeContextProvider
):
    """Simple in-memory knowledge provider."""

    def __init__(
        self,
        knowledge: dict[str, list[str]] | None = None,
    ) -> None:
        """Initialize knowledge store."""

        self._knowledge = (
            knowledge
            if knowledge is not None
            else {}
        )

    def retrieve(
        self,
        query: str,
    ) -> list[str]:
        """Retrieve matching knowledge."""

        return self._knowledge.get(
            query,
            [],
        )
