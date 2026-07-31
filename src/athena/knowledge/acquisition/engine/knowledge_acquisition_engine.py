"""
Athena Knowledge Acquisition Engine

Public entry point for AKC.
"""

from typing import Any

from .pass_manager import PassManager
from ..pipeline.pipeline import create_default_pipeline
from ..domain.knowledge_context import KnowledgeContext


class KnowledgeAcquisitionEngine:
    """
    Executes Athena knowledge compilation.
    """

    def __init__(
        self,
        pass_manager: PassManager | None = None,
    ) -> None:

        self.pass_manager = (
            pass_manager
            if pass_manager is not None
            else create_default_pipeline()
        )

    def compile(
        self,
        input_data: Any,
        context: KnowledgeContext | None = None,
    ) -> Any:
        """
        Compile input into Athena knowledge.
        """

        if context is None:
            context = KnowledgeContext()

        return self.pass_manager.execute(
            context,
            input_data,
        )