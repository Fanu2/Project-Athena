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

from .workflow import (
    AssistantWorkflowStep,
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

        workflow_steps: list[
            AssistantWorkflowStep
        ] = []

        if capability.requires_retrieval:
            steps.append(
                "retrieve_information"
            )

            workflow_steps.append(
                AssistantWorkflowStep(
                    name="retrieve_information",
                    description=(
                        "Search workspace documents "
                        "for relevant information"
                    ),
                    category="retrieval",
                )
            )

        if capability.requires_evidence:
            steps.append(
                "build_evidence"
            )

            workflow_steps.append(
                AssistantWorkflowStep(
                    name="build_evidence",
                    description=(
                        "Collect supporting evidence "
                        "from retrieved sources"
                    ),
                    category="evidence",
                )
            )

        if capability.name in (
            "summary",
            "explanation",
            "analysis",
        ):
            steps.append(
                "generate_response"
            )

            workflow_steps.append(
                AssistantWorkflowStep(
                    name="generate_response",
                    description=(
                        "Generate a grounded response "
                        "using available evidence"
                    ),
                    category="generation",
                )
            )

        if capability.requires_citations:
            steps.append(
                "attach_citations"
            )

            workflow_steps.append(
                AssistantWorkflowStep(
                    name="attach_citations",
                    description=(
                        "Attach citations to supporting "
                        "evidence sources"
                    ),
                    category="citation",
                )
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
            workflow_steps=tuple(workflow_steps),
        )