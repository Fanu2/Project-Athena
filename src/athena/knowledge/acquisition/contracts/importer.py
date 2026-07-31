"""
Athena Importer Contract

Defines how external sources are imported
into Athena ImportArtifacts.
"""

from abc import ABC, abstractmethod

from ..domain.knowledge_source import KnowledgeSource
from ..domain.import_artifact import ImportArtifact


class Importer(ABC):
    """
    Base contract for all Athena importers.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Importer identifier.
        """
        pass

    @property
    @abstractmethod
    def supported_types(self) -> list[str]:
        """
        Supported source types.
        """
        pass

    @abstractmethod
    def import_source(
        self,
        source: KnowledgeSource,
    ) -> ImportArtifact:
        """
        Convert source into ImportArtifact.
        """
        pass