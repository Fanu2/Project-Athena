"""
Athena Import Pass

First stage of Knowledge Compilation.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext


class ImportPass(PipelineStage):
    """
    Imports knowledge sources.

    Initial implementation:
    pass-through stage.
    """

    @property
    def name(self) -> str:
        return "import"

    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:
        """
        Execute import stage.
        """

        return input_data