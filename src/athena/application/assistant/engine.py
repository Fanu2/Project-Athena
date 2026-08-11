"""
Athena Assistant Engine.

Combines intent understanding,
capability routing,
workspace context,
and planning.
"""

from __future__ import annotations

from athena.ai.intent.service import (
    IntentService,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from .capability_registry import (
    CapabilityRegistry,
)

from .context import (
    AssistantContext,
)

from .decision import (
    AssistantDecision,
)

from .plan import (
    AssistantPlan,
)

from .planner import (
    AssistantPlanner,
)

from .workspace_context import (
    AssistantWorkspaceContext,
)


class AssistantEngine:
    """
    Coordinates Athena assistant decisions.
    """

    def __init__(
        self,
        intent_service: IntentService,
    ) -> None:

        self._intent_service = (
            intent_service
        )

        self._registry = (
            CapabilityRegistry()
        )

        self._planner = (
            AssistantPlanner()
        )

        self._workspace_context: (
            AssistantWorkspaceContext | None
        ) = None


    def analyze_request(
        self,
        query: str,
        workspace: WorkspaceIntelligenceSnapshot,
    ) -> AssistantDecision:
        """
        Analyze request and create decision.
        """

        intent = (
            self._intent_service.detect(
                query,
            )
        )

        context = AssistantContext(
            intent=intent,
            workspace=workspace,
        )

        self._workspace_context = (
            AssistantWorkspaceContext(
                workspace_name=(
                    workspace.workspace_name
                ),
                document_count=(
                    workspace.document_count
                ),
                knowledge_item_count=(
                    workspace.knowledge_item_count
                ),
                conversation_messages=(
                    workspace.conversation_messages
                ),
            )
        )

        return self._decide(
            context,
        )


    def create_plan(
        self,
        decision: AssistantDecision,
    ) -> AssistantPlan:
        """
        Create a non-executing assistant plan.
        """

        return self._planner.create_plan(
            decision.capability,
            self._workspace_context,
        )


    def _decide(
        self,
        context: AssistantContext,
    ) -> AssistantDecision:
        """
        Create assistant decision.
        """

        capability = (
            self._registry.resolve(
                context.intent.intent,
            )
        )

        return AssistantDecision(
            intent=context.intent.intent,
            capability=capability,
            confidence=context.intent.confidence,
        )