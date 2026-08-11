"""
Athena Assistant Engine.

Combines intent understanding,
capability routing,
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
