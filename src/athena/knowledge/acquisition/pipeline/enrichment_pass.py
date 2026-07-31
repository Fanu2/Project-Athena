
"""
Athena Enrichment Pass

Adds derived intelligence to knowledge.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext


class EnrichmentPass(PipelineStage):
    """
    Knowledge enrichment compiler stage.

    Initial implementation:
    pass-through until enrichers
    are connected.
    """

    @property
    def name(self) -> str:
        return "enrichment"

    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:
        """
        Execute enrichment stage.
        """

        return input_data