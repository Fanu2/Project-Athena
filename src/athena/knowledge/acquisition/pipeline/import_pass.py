
"""
Athena Import Pass

Acquires external knowledge and converts
it into compiler representations.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext
from ..adapters.artifact_adapter import ArtifactAdapter


class ImportPass(PipelineStage):
    """
    First AKC compiler stage.

    Responsibilities:
    - acquire source
    - create ImportArtifact
    - convert to KnowledgeRepresentation
    """

    def __init__(self) -> None:
        self._adapter = ArtifactAdapter()

    @property
    def name(self) -> str:
        return "import"

    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:

        provider_manager = context.get_service(
            "provider_manager"
        )

        if provider_manager is None:
            return input_data

        artifact = provider_manager.execute(
            "document_structure_extraction",
            input_data,
        )

        return self._adapter.adapt(
            artifact
        )