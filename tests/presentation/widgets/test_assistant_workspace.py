"""
Tests for assistant workspace widget.
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


def test_assistant_workspace_contains_components(
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

    assert (
        widget.session_widget
        is not None
    )

    assert (
        widget.conversation_widget
        is not None
    )

    assert (
        widget.plan_widget
        is not None
    )
