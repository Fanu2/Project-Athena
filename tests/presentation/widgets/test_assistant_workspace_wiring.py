"""
Tests assistant workspace wiring.
"""

from athena.ai.intent.service import (
    IntentService,
)

from athena.application.assistant.engine import (
    AssistantEngine,
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

    service = AssistantWorkspaceService(
        AssistantEngine(
            IntentService(),
        ),
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
        document_count=10,
        knowledge_item_count=5,
        conversation_messages=2,
    )

    plan = widget.create_plan(
        "summarize documents",
        workspace,
    )

    assert (
        plan.capability
        == "summary"
    )

    assert (
        "summary"
        in widget.plan_widget.content.text()
    )
