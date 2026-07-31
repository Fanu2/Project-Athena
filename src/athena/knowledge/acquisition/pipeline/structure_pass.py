"""
Athena Structure Pass

Transforms imported artifacts into
Knowledge Representation Models.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext
from ..domain.knowledge_representation import KnowledgeRepresentation


class StructurePass(PipelineStage):
    """
    Builds structural representation.

    Initial implementation:
    creates a basic KRM container.
    """

    @property
    def name(self) -> str:
        return "structure"

    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:
        """
        Convert input into structural representation.
        """

        if isinstance(
            input_data,
            KnowledgeRepresentation,
        ):
            return input_data

        return KnowledgeRepresentation(
            representation_type="generic",
            title=str(input_data),
        )