"""
Assistant execution planning models.
"""

from __future__ import annotations

from dataclasses import dataclass

from .validation import (
    AssistantPlanValidation,
)

from .workflow import (
    AssistantWorkflowStep,
)


@dataclass(frozen=True, slots=True)
class AssistantPlan:
    """
    Describes the steps required for an assistant task.
    """

    capability: str

    steps: tuple[str, ...]

    context_notes: tuple[str, ...] = ()

    workflow_steps: tuple[
        AssistantWorkflowStep,
        ...
    ] = ()

    validation: AssistantPlanValidation | None = None