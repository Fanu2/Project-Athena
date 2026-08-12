"""
Tests for assistant recovery widget.
"""

from athena.application.assistant.session import (
    create_assistant_session,
)

from athena.presentation.widgets.assistant_recovery import (
    AssistantRecoveryWidget,
)


def test_recovery_widget_displays_sessions(
    qtbot,
):

    widget = AssistantRecoveryWidget()

    qtbot.addWidget(
        widget,
    )

    session = create_assistant_session(
        workspace_id="workspace-001",
        workspace_name="Research",
        conversation_id="conv-001",
    )

    widget.set_sessions(
        (
            session,
        ),
    )

    assert (
        widget.sessions.count()
        == 1
    )
