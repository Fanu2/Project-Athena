"""
Athena Pass Manager

Controls ordered execution of Knowledge Compiler stages.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext


class PassManager:
    """
    Executes registered compiler stages sequentially.

    The PassManager does not know about:
        - PDFs
        - OCR
        - LLMs
        - Providers

    It only manages execution flow.
    """

    def __init__(self) -> None:
        self._stages: list[PipelineStage] = []

    def register(
        self,
        stage: PipelineStage,
    ) -> None:
        """
        Register a compiler stage.
        """
        self._stages.append(stage)

    @property
    def stages(self) -> list[PipelineStage]:
        """
        Return registered stages.
        """
        return self._stages

    def execute(
        self,
        context: KnowledgeContext,
        data: Any,
    ) -> Any:
        """
        Execute all registered stages.
        """

        result = data

        for stage in self._stages:
            result = stage.execute(
                context,
                result,
            )

        return result