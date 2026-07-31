"""
Athena Validator Contract

Defines validation of knowledge candidates
before canonical knowledge creation.
"""

from abc import ABC, abstractmethod

from ..domain.knowledge_candidate import KnowledgeCandidate
from ..domain.evidence_record import EvidenceRecord
from ..domain.knowledge_context import KnowledgeContext


class Validator(ABC):
    """
    Base contract for knowledge validation.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Validator identifier.
        """
        pass

    @abstractmethod
    def validate(
        self,
        candidate: KnowledgeCandidate,
        evidence: list[EvidenceRecord],
        context: KnowledgeContext,
    ) -> bool:
        """
        Validate a knowledge candidate.

        Returns:
            True  - candidate accepted
            False - candidate rejected
        """
        pass