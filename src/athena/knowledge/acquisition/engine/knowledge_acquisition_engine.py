"""
Athena Knowledge Acquisition Engine

Public entry point for AKC.
"""

from typing import Any

from .pass_manager import PassManager
from ..pipeline.pipeline import create_default_pipeline
from ..domain.knowledge_context import KnowledgeContext
from ..domain.compilation_report import (
    CompilationReport,
)


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

    def compile_with_report(
        self,
        input_data: Any,
        context: KnowledgeContext | None = None,
    ) -> tuple[Any, CompilationReport]:
        """
        Compile input and return execution report.
        """

        if context is None:
            context = KnowledgeContext()

        report = CompilationReport(
            source=input_data,
        )

        try:

            result = self.pass_manager.execute(
                context,
                input_data,
            )

            report.stages = (
                self.pass_manager.execution_records.copy()
            )

            if isinstance(
                result,
                list,
            ):
                report.objects_created = len(result)

            report.complete()

            return result, report

        except Exception as exc:

            report.status = "failed"

            report.error = (
                f"{type(exc).__name__}: {exc}"
            )

            report.stages = (
                self.pass_manager.execution_records.copy()
            )

            report.complete()

            raise