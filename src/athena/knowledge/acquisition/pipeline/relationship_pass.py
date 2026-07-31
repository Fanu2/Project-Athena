"""
Athena Relationship Pass

Creates semantic relationships between
knowledge entities.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext


class RelationshipPass(PipelineStage):
    """
    Relationship extraction compiler stage.

    Initial implementation:
    pass-through stage until
    RelationshipExtractor providers are connected.
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
        Execute relationship extraction.
        """

        return input_data