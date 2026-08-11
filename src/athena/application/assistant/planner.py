"""
Assistant capability planner.

Converts capabilities into execution plans.
"""

from __future__ import annotations

from .capability import (
    AssistantCapability,
)

from .plan import (
    AssistantPlan,
)


class AssistantPlanner:
    """
    Creates non-executing assistant plans.
    """

    def create_plan(
        self,
        capability: AssistantCapability,
    ) -> AssistantPlan:
        """
        Create a plan from a capability.
        """

        steps: list[str] = []

        if capability.requires_retrieval:
            steps.append(
                "retrieve_information"
            )

        if capability.requires_evidence:
            steps.append(
                "build_evidence"
            )

        if capability.name in (
            "summary",
            "explanation",
            "analysis",
        ):
            steps.append(
                "generate_response"
            )

        if capability.requires_citations:
            steps.append(
                "attach_citations"
            )

        return AssistantPlan(
            capability=capability.name,
            steps=tuple(steps),
        )
