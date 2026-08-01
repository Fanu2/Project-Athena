"""
Athena Index Pass

Indexes canonical knowledge through
registered indexing adapters.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext
from ..domain.knowledge_object import KnowledgeObject


class IndexPass(PipelineStage):
    """
    Final compiler stage.

    Sends canonical knowledge to
    indexing services.
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
        Index knowledge objects.
        """

        indexer = context.get_service(
            "knowledge_indexer"
        )

        if indexer is None:
            return input_data

        if not isinstance(
            input_data,
            list,
        ):
            return input_data

        for knowledge in input_data:

            if isinstance(
                knowledge,
                KnowledgeObject,
            ):
                indexer.index(
                    knowledge
                )

        return input_data