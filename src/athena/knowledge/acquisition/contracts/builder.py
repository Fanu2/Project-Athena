"""
Athena Knowledge Builder Contract

Defines creation of canonical Knowledge Objects
from validated knowledge candidates.
"""

from abc import ABC, abstractmethod

from ..domain.knowledge_candidate import KnowledgeCandidate
from ..domain.knowledge_context import KnowledgeContext
from ..domain.knowledge_object import KnowledgeObject
from ..domain.evidence_record import EvidenceRecord


class Builder(ABC):
    """
    Base contract for Knowledge Object builders.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Builder identifier.
        """
        pass

    @property
    @abstractmethod
    def supported_types(self) -> list[str]:
        """
        Supported knowledge object types.
        """
        pass

    @abstractmethod
    def build(
        self,
        candidate: KnowledgeCandidate,
        evidence: list[EvidenceRecord],
        context: KnowledgeContext,
    ) -> KnowledgeObject:
        """
        Convert candidate into canonical knowledge.
        """
        pass