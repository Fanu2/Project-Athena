"""
Athena Structure Pass

Creates structural knowledge nodes
from Knowledge Representation Model.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext
from ..domain.knowledge_representation import (
    KnowledgeRepresentation,
)
from ..domain.knowledge_node import KnowledgeNode


class StructurePass(PipelineStage):
    """
    Builds structural nodes inside KRM.
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
        Build document structure.
        """

        if not isinstance(
            input_data,
            KnowledgeRepresentation,
        ):
            return input_data

        document_node = KnowledgeNode(
            node_type="document",
            content=input_data.title,
        )

        document_node.add_metadata(
            "representation_id",
            str(
                input_data.representation_id
            ),
        )

        input_data.add_node(
            document_node.node_id
        )

        return input_data