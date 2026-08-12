"""
Assistant workspace orchestration service.

Coordinates assistant requests,
planning, and workspace context.
"""

from __future__ import annotations

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from .engine import (
    AssistantEngine,
)

from .plan import (
    AssistantPlan,
)


class AssistantWorkspaceService:
    """
    Coordinates workspace assistant workflows.
    """

    def __init__(
        self,
        assistant_engine: AssistantEngine,
    ) -> None:

        self._assistant_engine = (
            assistant_engine
        )


    def create_plan(
        self,
        query: str,
        workspace: WorkspaceIntelligenceSnapshot,
    ) -> AssistantPlan:
        """
        Analyze request and create assistant plan.
        """

        decision = (
            self._assistant_engine.analyze_request(
                query,
                workspace,
            )
        )

        return (
            self._assistant_engine.create_plan(
                decision,
            )
        )
