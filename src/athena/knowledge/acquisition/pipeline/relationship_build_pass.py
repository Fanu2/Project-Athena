"""
Athena Relationship Build Pass

Converts candidate relationships into
canonical KnowledgeRelationships.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext

from ..domain.knowledge_candidate_relationship import (
    KnowledgeCandidateRelationship,
)

from ..domain.knowledge_relationship import (
    KnowledgeRelationship,
)


class RelationshipBuildPass(PipelineStage):
    """
    Converts temporary relationships into
    canonical relationships.
    """

    @property
    def name(self) -> str:
        return "relationship_build"

    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:
        """
        Build canonical relationships.
        """

        if not isinstance(
            input_data,
            list,
        ):
            return input_data

        repository = (
            context.get_service(
                "relationship_repository"
            )
        )

        relationships = []

        for candidate in input_data:

            if not isinstance(
                candidate,
                KnowledgeCandidateRelationship,
            ):
                continue

            relationship = KnowledgeRelationship(
                relationship_type=(
                    candidate.relationship_type
                ),
                confidence=(
                    candidate.confidence
                ),
                metadata=(
                    candidate.metadata.copy()
                ),
            )

            if repository is not None:

                repository.save(
                    relationship
                )

            relationships.append(
                relationship
            )

        return relationships