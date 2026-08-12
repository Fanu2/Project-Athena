"""
Assistant execution planning models.
"""

from __future__ import annotations

from dataclasses import dataclass

from .action import (
    AssistantAction,
)

from .validation import (
    AssistantPlanValidation,
)

from .workflow import (
    AssistantWorkflowStep,
)


@dataclass(frozen=True, slots=True)
class AssistantPlan:
    """
    Describes the steps and actions
    required for an assistant task.
    """

    capability: str

    steps: tuple[str, ...]

    context_notes: tuple[str, ...] = ()

    workflow_steps: tuple[
        AssistantWorkflowStep,
        ...
    ] = ()

    actions: tuple[
        AssistantAction,
        ...
    ] = ()

    validation: AssistantPlanValidation | None = None