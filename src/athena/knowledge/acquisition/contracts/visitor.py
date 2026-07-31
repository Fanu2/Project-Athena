"""
Athena Visitor Contract

Defines traversal operations over
Knowledge Representation structures.
"""

from abc import ABC, abstractmethod

from ..domain.knowledge_node import KnowledgeNode
from ..domain.knowledge_context import KnowledgeContext


class Visitor(ABC):
    """
    Base contract for KRM visitors.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Visitor identifier.
        """
        pass

    @abstractmethod
    def visit(
        self,
        node: KnowledgeNode,
        context: KnowledgeContext,
    ) -> None:
        """
        Process a knowledge node.
        """
        pass