"""
Athena Semantic Pass

Creates semantic knowledge candidates
from structural knowledge nodes.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext
from ..domain.knowledge_representation import (
    KnowledgeRepresentation,
)
from ..domain.knowledge_candidate import (
    KnowledgeCandidate,
)


class SemanticPass(PipelineStage):
    """
    Converts structural knowledge into
    semantic candidates.

    Preserves source provenance metadata
    for downstream knowledge objects.
    """

    @property
    def name(self) -> str:
        return "semantic"

    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:
        """
        Generate knowledge candidates.
        """

        if not isinstance(
            input_data,
            KnowledgeRepresentation,
        ):
            return input_data

        candidates = []

        for node_id in input_data.nodes:

            candidate = KnowledgeCandidate(
                candidate_type=(
                    input_data.representation_type
                ),
                value=input_data.title,
                source_node_id=node_id,
                confidence=0.5,
            )

            #
            # Preserve compilation provenance
            #

            candidate.add_metadata(
                "representation_id",
                str(
                    input_data.representation_id
                ),
            )

            candidate.add_metadata(
                "provider",
                input_data.metadata.get(
                    "provider"
                ),
            )

            candidate.add_metadata(
                "extraction_method",
                input_data.metadata.get(
                    "extraction_method"
                ),
            )

            candidate.add_metadata(
                "source_path",
                input_data.metadata.get(
                    "source_path"
                ),
            )

            candidates.append(
                candidate
            )

        return candidates