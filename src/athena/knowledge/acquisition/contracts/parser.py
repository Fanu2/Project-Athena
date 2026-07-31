"""
Athena Parser Contract

Defines how imported artifacts are transformed
into Knowledge Representation Models.
"""

from abc import ABC, abstractmethod

from ..domain.import_artifact import ImportArtifact
from ..domain.knowledge_context import KnowledgeContext
from ..domain.knowledge_representation import KnowledgeRepresentation


class Parser(ABC):
    """
    Base contract for Athena parsers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Parser identifier.
        """
        pass

    @property
    @abstractmethod
    def supported_types(self) -> list[str]:
        """
        Supported artifact types.
        """
        pass

    @abstractmethod
    def parse(
        self,
        artifact: ImportArtifact,
        context: KnowledgeContext,
    ) -> KnowledgeRepresentation:
        """
        Convert artifact into KRM.
        """
        pass