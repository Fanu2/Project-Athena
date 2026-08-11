"""
Assistant plan presentation.
"""

from __future__ import annotations

from .plan import AssistantPlan


class AssistantPlanPresenter:
    """
    Converts assistant plans into
    human-readable explanations.
    """

    def present(
        self,
        plan: AssistantPlan,
    ) -> str:
        """
        Present a plan.
        """

        lines = [
            "Athena Plan",
            "",
            f"Capability: {plan.capability}",
            "",
            "Steps:",
        ]

        for index, step in enumerate(
            plan.steps,
            start=1,
        ):
            lines.append(
                f"{index}. {step.replace('_', ' ')}"
            )

        return "\n".join(lines)
