"""
Athena Extractor Contract

Defines semantic extraction from
Knowledge Representation Models.
"""

from abc import ABC, abstractmethod

from ..domain.knowledge_context import KnowledgeContext
from ..domain.knowledge_representation import KnowledgeRepresentation
from ..domain.knowledge_candidate import KnowledgeCandidate


class Extractor(ABC):
    """
    Base contract for semantic extractors.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Extractor identifier.
        """
        pass

    @property
    @abstractmethod
    def supported_types(self) -> list[str]:
        """
        Supported extraction domains.
        """
        pass

    @abstractmethod
    def extract(
        self,
        representation: KnowledgeRepresentation,
        context: KnowledgeContext,
    ) -> list[KnowledgeCandidate]:
        """
        Extract knowledge candidates.
        """
        pass