"""
Athena Pass Manager

Controls ordered execution of Knowledge Compiler stages.
"""

from datetime import datetime, timezone
from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext
from ..domain.stage_execution_record import (
    StageExecutionRecord,
)

from ..exceptions.exceptions import (
    PipelineExecutionError,
)


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

        self.execution_records: list[
            StageExecutionRecord
        ] = []

    def register(
        self,
        stage: PipelineStage,
    ) -> None:
        """
        Register a compiler stage.
        """

        self._stages.append(
            stage
        )

    @property
    def stages(
        self,
    ) -> list[PipelineStage]:
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

        Temporary tracing enabled to locate
        pipeline regression.
        """

        result = data

        self.execution_records.clear()

        for stage in self._stages:

            print(
                f"\n========== {stage.name} INPUT =========="
            )

            print(
                type(result).__name__
            )

            print(
                result
            )

            record = StageExecutionRecord(
                stage_name=stage.name,
                input_type=type(result).__name__,
            )

            try:

                result = stage.execute(
                    context,
                    result,
                )

                record.output_type = (
                    type(result).__name__
                )

            except Exception as exc:

                record.status = "failed"

                record.error = (
                    f"{type(exc).__name__}: {exc}"
                )

                record.completed_at = (
                    datetime.now(timezone.utc)
                )

                self.execution_records.append(
                    record
                )

                raise PipelineExecutionError(
                    stage_name=stage.name,
                    input_type=type(result).__name__,
                    message=str(exc),
                ) from exc

            record.completed_at = (
                datetime.now(timezone.utc)
            )

            self.execution_records.append(
                record
            )

            print(
                f"\n========== {stage.name} OUTPUT =========="
            )

            print(
                type(result).__name__
            )

            print(
                result
            )

        return result