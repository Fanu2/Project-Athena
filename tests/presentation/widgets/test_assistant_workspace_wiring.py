"""
Tests for assistant workspace wiring.
"""

from athena.ai.intent.service import (
    IntentService,
)

from athena.ai.intent.models import (
    IntentType,
)

from athena.application.assistant.engine import (
    AssistantEngine,
)

from athena.application.assistant.in_memory_session_store import (
    InMemoryAssistantSessionStore,
)

from athena.application.assistant.recovery_service import (
    AssistantRecoveryService,
)

from athena.application.assistant.workspace_service import (
    AssistantWorkspaceService,
)

from athena.presentation.widgets.assistant_workspace import (
    AssistantWorkspaceWidget,
)


from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)


def test_workspace_widget_creates_plan(
    qtbot,
):

    recovery_service = AssistantRecoveryService(
        InMemoryAssistantSessionStore(),
    )

    service = AssistantWorkspaceService(
        AssistantEngine(
            IntentService(),
        ),
        recovery_service,
    )

    widget = AssistantWorkspaceWidget(
        service,
    )

    qtbot.addWidget(
        widget,
    )

    workspace = WorkspaceIntelligenceSnapshot(
        workspace_id="workspace-001",
        workspace_name="Research",
        document_count=1,
        knowledge_item_count=0,
        conversation_messages=0,
    )

    plan = service.create_plan(
        "search documents",
        workspace,
    )

    assert plan is not None
