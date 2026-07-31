"""
Athena Index Pass

Creates index representations from
canonical knowledge.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext


class IndexPass(PipelineStage):
    """
    Knowledge indexing compiler stage.

    Initial implementation:
    pass-through until indexers
    are connected.
    """

    @property
    def name(self) -> str:
        return "index"

    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:
        """
        Execute indexing stage.
        """

        return input_data