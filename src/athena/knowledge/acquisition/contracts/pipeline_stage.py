"""
Athena Pipeline Stage Contract

Defines the interface for every
Knowledge Compiler processing stage.
"""

from abc import ABC, abstractmethod
from typing import Any

from ..domain.knowledge_context import KnowledgeContext


class PipelineStage(ABC):
    """
    Base contract for AKC compiler stages.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Stage identifier.
        """
        pass

    @abstractmethod
    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:
        """
        Execute transformation.
        """
        pass