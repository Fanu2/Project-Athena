"""
Athena Relationship Pass

Creates semantic candidate relationships
without interrupting the main compiler stream.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext

from ..domain.knowledge_candidate import (
    KnowledgeCandidate,
)

from ..domain.knowledge_candidate_relationship import (
    KnowledgeCandidateRelationship,
)


class RelationshipPass(PipelineStage):
    """
    Builds candidate relationships as
    compiler side output.
    """

    @property
    def name(self) -> str:
        return "relationship"

    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:
        """
        Create candidate relationships.

        The original candidate stream is
        preserved for BuildPass.
        """

        if not isinstance(
            input_data,
            list,
        ):
            return input_data

        candidates = [
            item
            for item in input_data
            if isinstance(
                item,
                KnowledgeCandidate,
            )
        ]

        relationships = []

        for index, source in enumerate(candidates):

            for target in candidates[index + 1:]:

                relationship = (
                    KnowledgeCandidateRelationship(
                        source_candidate_id=(
                            source.candidate_id
                        ),
                        target_candidate_id=(
                            target.candidate_id
                        ),
                    )
                )

                relationships.append(
                    relationship
                )

        #
        # Store as side output
        #

        context.add_metadata(
            "candidate_relationships",
            relationships,
        )

        #
        # Preserve compiler stream
        #

        return input_data