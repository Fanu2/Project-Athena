"""
Athena Indexer Contract

Defines indexing capability used by AKC.
"""

from abc import ABC, abstractmethod
from typing import Any


class Indexer(ABC):
    """
    Base indexing contract.
    """

    @abstractmethod
    def index(
        self,
        knowledge: Any,
    ) -> Any:
        """
        Index canonical knowledge.
        """

        raise NotImplementedError