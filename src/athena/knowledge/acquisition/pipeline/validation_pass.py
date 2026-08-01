"""
Athena Validation Pass

Validates knowledge candidates
before canonical creation.
"""

from typing import Any

from ..contracts.pipeline_stage import PipelineStage
from ..domain.knowledge_context import KnowledgeContext
from ..domain.knowledge_candidate import KnowledgeCandidate
from ..domain.validation_result import ValidationResult
from ..validators.default_validator import (
    DefaultValidator,
)


class ValidationPass(PipelineStage):
    """
    Candidate validation stage.
    """

    def __init__(self):
        self._validator = DefaultValidator()

    @property
    def name(self) -> str:
        return "validation"

    def execute(
        self,
        context: KnowledgeContext,
        input_data: Any,
    ) -> Any:

        if not isinstance(
            input_data,
            list,
        ):
            return input_data

        accepted = []

        for candidate in input_data:

            if (
                isinstance(
                    candidate,
                    KnowledgeCandidate,
                )
                and self._validator.validate(
                    candidate
                )
            ):
                accepted.append(candidate)

        return accepted