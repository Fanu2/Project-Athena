"""
Assistant quality evaluation service.
"""

from __future__ import annotations

from .plan import (
    AssistantPlan,
)

from .validation import (
    AssistantPlanValidation,
)


class AssistantQualityService:
    """
    Validates assistant plans.
    """

    def validate(
        self,
        plan: AssistantPlan,
    ) -> AssistantPlanValidation:
        """
        Validate plan completeness.
        """

        checks: list[str] = []

        warnings: list[str] = []

        valid = True

        if plan.capability:
            checks.append(
                "capability_available"
            )
        else:
            valid = False
            warnings.append(
                "missing_capability"
            )

        if (
            plan.workflow_steps
            or plan.steps
        ):
            checks.append(
                "workflow_present"
            )
        else:
            valid = False
            warnings.append(
                "missing_workflow"
            )

        if plan.context_notes:
            checks.append(
                "context_available"
            )
        else:
            warnings.append(
                "missing_context"
            )

        return AssistantPlanValidation(
            valid=valid,
            checks=tuple(checks),
            warnings=tuple(warnings),
        )
