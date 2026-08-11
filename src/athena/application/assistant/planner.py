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

from .workspace_context import (
    AssistantWorkspaceContext,
)


class AssistantPlanner:
    """
    Creates non-executing assistant plans.
    """

    def create_plan(
        self,
        capability: AssistantCapability,
        context: AssistantWorkspaceContext | None = None,
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

        context_notes: list[str] = []

        if context is not None:
            context_notes.append(
                f"Workspace: {context.workspace_name}"
            )

            context_notes.append(
                f"Documents available: {context.document_count}"
            )

            context_notes.append(
                f"Knowledge items: {context.knowledge_item_count}"
            )

            context_notes.append(
                f"Conversation messages: {context.conversation_messages}"
            )

        return AssistantPlan(
            capability=capability.name,
            steps=tuple(steps),
            context_notes=tuple(context_notes),
        )