"""
Athena Assistant Engine.

Combines intent understanding,
capability routing,
workspace context,
planning,
execution boundaries,
and quality validation.
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

from .execution import (
    AssistantExecutionRequest,
)

from .plan import (
    AssistantPlan,
)

from .planner import (
    AssistantPlanner,
)

from .quality import (
    AssistantQualityService,
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

        self._quality_service = (
            AssistantQualityService()
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


    def create_execution_request(
        self,
        plan: AssistantPlan,
    ) -> AssistantExecutionRequest:
        """
        Wrap a plan for future execution.

        Execution is handled separately.
        """

        return AssistantExecutionRequest(
            plan=plan,
        )


    def validate_plan(
        self,
        plan: AssistantPlan,
    ):
        """
        Validate assistant plan quality.
        """

        return self._quality_service.validate(
            plan,
        )


    def attach_validation(
        self,
        plan: AssistantPlan,
    ) -> AssistantPlan:
        """
        Attach quality diagnostics to plan.
        """

        validation = (
            self.validate_plan(
                plan,
            )
        )

        return AssistantPlan(
            capability=plan.capability,
            steps=plan.steps,
            context_notes=plan.context_notes,
            workflow_steps=plan.workflow_steps,
            validation=validation,
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