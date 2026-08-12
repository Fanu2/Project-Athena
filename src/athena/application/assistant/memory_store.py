"""
Assistant memory store boundary.

Defines explicit user-controlled memory operations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from .memory import (
    AssistantMemoryItem,
)


class AssistantMemoryStore(ABC):
    """
    Boundary for assistant memory persistence.
    """

    @abstractmethod
    def save(
        self,
        item: AssistantMemoryItem,
    ) -> None:
        """
        Store a memory item.
        """
        raise NotImplementedError


    @abstractmethod
    def retrieve(
        self,
        key: str,
    ) -> AssistantMemoryItem | None:
        """
        Retrieve a memory item.
        """
        raise NotImplementedError


    @abstractmethod
    def delete(
        self,
        key: str,
    ) -> None:
        """
        Delete a memory item.
        """
        raise NotImplementedError
