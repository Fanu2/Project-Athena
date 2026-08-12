"""
Assistant workspace orchestration service.

Coordinates assistant requests,
planning, workspace context,
and session recovery.
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

from .recovery_service import (
    AssistantRecoveryService,
)

from .session import (
    AssistantSession,
)


class AssistantWorkspaceService:
    """
    Coordinates workspace assistant workflows.
    """

    def __init__(
        self,
        assistant_engine: AssistantEngine,
        recovery_service: AssistantRecoveryService,
    ) -> None:

        self._assistant_engine = (
            assistant_engine
        )

        self._recovery_service = (
            recovery_service
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


    def restore_session(
        self,
        session_id: str,
    ) -> AssistantSession | None:
        """
        Restore previous assistant session.
        """

        return (
            self._recovery_service.restore(
                session_id,
            )
        )


    def available_sessions(
        self,
    ) -> tuple[
        AssistantSession,
        ...
    ]:
        """
        Return recoverable sessions.
        """

        return (
            self._recovery_service.available_sessions()
        )
