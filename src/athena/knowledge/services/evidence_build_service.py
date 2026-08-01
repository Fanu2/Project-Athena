"""
Athena Evidence Build Service

Creates evidence records from
compiled knowledge objects.
"""

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)

from athena.knowledge.repositories.evidence_repository import (
    EvidenceRepository,
)


class EvidenceBuildService:
    """
    Builds and stores evidence records.
    """

    def __init__(
        self,
        repository: EvidenceRepository,
    ) -> None:

        self._repository = repository

    def build(
        self,
        knowledge_object: KnowledgeObject,
    ) -> EvidenceRecord:
        """
        Create evidence for knowledge object.
        """

        evidence = EvidenceRecord(
            source_id=(
                knowledge_object.object_id
            ),
            source_reference=(
                knowledge_object.metadata.get(
                    "source_path"
                )
            ),
            extraction_method=(
                knowledge_object.metadata.get(
                    "extraction_method"
                )
            ),
            provider=(
                knowledge_object.metadata.get(
                    "provider"
                )
            ),
            confidence=(
                knowledge_object.confidence
            ),
            metadata={
                "knowledge_object_id": str(
                    knowledge_object.object_id
                ),
                "object_type": (
                    knowledge_object.object_type
                ),
            },
        )

        self._repository.save(
            evidence
        )

        return evidence