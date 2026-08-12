"""
Athena Assistant Engine.

Combines intent understanding,
capability routing,
workspace context,
memory context,
session context,
action planning,
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

from .action_registry import (
    ActionRegistry,
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

from .memory import (
    AssistantMemoryItem,
)

from .memory_store import (
    AssistantMemoryStore,
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

from .session import (
    AssistantSession,
)

from .session_store import (
    AssistantSessionStore,
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

        self._action_registry = (
            ActionRegistry()
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

        self._memory_store: (
            AssistantMemoryStore | None
        ) = None

        self._memories: tuple[
            AssistantMemoryItem,
            ...
        ] = ()

        self._session_store: (
            AssistantSessionStore | None
        ) = None

        self._session: (
            AssistantSession | None
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
            memories=self._memories,
            session=self._session,
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

                #
                # A20.4 Workspace Intelligence Context
                #
                # Use safe access so older callers
                # passing Workspace objects continue
                # to work.
                #

                recent_documents=(
                    getattr(
                        workspace,
                        "recent_documents",
                        (),
                    )
                ),

                recent_queries=(
                    getattr(
                        workspace,
                        "recent_queries",
                        (),
                    )
                ),

                recent_sessions=(
                    getattr(
                        workspace,
                        "recent_sessions",
                        (),
                    )
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

        actions = (
            self._action_registry.resolve(
                decision.capability,
            )
        )

        return self._planner.create_plan(
            decision.capability,
            self._workspace_context,
            self._memories,
            actions,
        )


    def create_execution_request(
        self,
        plan: AssistantPlan,
    ) -> AssistantExecutionRequest:
        """
        Wrap a plan for future execution.
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
            actions=plan.actions,
            validation=validation,
        )


    #
    # Memory Boundary (A22.12)
    #

    def set_memory_store(
        self,
        store: AssistantMemoryStore,
    ) -> None:
        """
        Attach explicit memory store.
        """

        self._memory_store = store


    def set_memories(
        self,
        memories: tuple[
            AssistantMemoryItem,
            ...
        ],
    ) -> None:
        """
        Attach explicit user-approved memories.
        """

        self._memories = memories


    def load_memory(
        self,
        key: str,
    ) -> AssistantMemoryItem | None:
        """
        Retrieve explicit user memory.
        """

        if self._memory_store is None:
            return None

        return self._memory_store.retrieve(
            key,
        )


    def load_memories(
        self,
        keys: tuple[str, ...],
    ) -> tuple[
        AssistantMemoryItem,
        ...
    ]:

        memories: list[
            AssistantMemoryItem
        ] = []

        if self._memory_store is None:
            return tuple(memories)

        for key in keys:

            memory = (
                self._memory_store.retrieve(
                    key,
                )
            )

            if memory is not None:
                memories.append(
                    memory,
                )

        return tuple(memories)


    #
    # Session Boundary (A22.16)
    #

    def set_session_store(
        self,
        store: AssistantSessionStore,
    ) -> None:
        """
        Attach assistant session storage.
        """

        self._session_store = store


    def set_session(
        self,
        session: AssistantSession,
    ) -> None:
        """
        Attach active assistant session.
        """

        self._session = session


    def get_session(
        self,
    ) -> AssistantSession | None:
        """
        Return active assistant session.
        """

        return self._session


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
