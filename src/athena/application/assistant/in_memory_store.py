"""
In-memory assistant memory store.

Used for testing only.
"""

from __future__ import annotations

from .memory import (
    AssistantMemoryItem,
)

from .memory_store import (
    AssistantMemoryStore,
)


class InMemoryAssistantMemoryStore(
    AssistantMemoryStore,
):
    """
    Temporary memory store.
    """

    def __init__(
        self,
    ) -> None:

        self._items: dict[
            str,
            AssistantMemoryItem,
        ] = {}


    def save(
        self,
        item: AssistantMemoryItem,
    ) -> None:

        self._items[item.key] = item


    def retrieve(
        self,
        key: str,
    ) -> AssistantMemoryItem | None:

        return self._items.get(
            key,
        )


    def delete(
        self,
        key: str,
    ) -> None:

        self._items.pop(
            key,
            None,
        )
