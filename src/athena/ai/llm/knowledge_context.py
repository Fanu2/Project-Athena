"""
Knowledge context provider interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class KnowledgeContextProvider(ABC):
    """Provide knowledge context for conversations."""

    @abstractmethod
    def retrieve(
        self,
        query: str,
    ) -> list[str]:
        """Retrieve relevant knowledge."""
