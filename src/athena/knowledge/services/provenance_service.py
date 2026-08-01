"""
Athena Provenance Service

Provides provenance information
for canonical knowledge objects.
"""

from typing import Any

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


class ProvenanceService:
    """
    Extracts provenance details from
    KnowledgeObject metadata.
    """

    def get_provenance(
        self,
        knowledge_object: KnowledgeObject,
    ) -> dict[str, Any]:
        """
        Return provenance information.
        """

        return {
            "object_id": str(
                knowledge_object.object_id
            ),
            "source_candidate_id": (
                knowledge_object.metadata.get(
                    "source_candidate_id"
                )
            ),
            "source_reference": (
                knowledge_object.metadata.get(
                    "source_reference"
                )
            ),
            "provider": (
                knowledge_object.metadata.get(
                    "provider"
                )
            ),
            "extraction_method": (
                knowledge_object.metadata.get(
                    "extraction_method"
                )
            ),
            "confidence": (
                knowledge_object.confidence
            ),
        }