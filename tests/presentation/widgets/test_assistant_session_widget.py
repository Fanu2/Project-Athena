"""
Tests for assistant session widget.
"""

from athena.application.assistant.session import (
    create_assistant_session,
)

from athena.presentation.widgets.assistant_session import (
    AssistantSessionWidget,
)


def test_session_widget_displays_session(
    qtbot,
):

    widget = AssistantSessionWidget()

    qtbot.addWidget(
        widget,
    )

    session = create_assistant_session(
        workspace_name="Research",
        conversation_id="conv-001",
    )

    widget.set_session(
        session,
    )

    text = widget.content.text()

    assert (
        "Research"
        in text
    )

    assert (
        "conv-001"
        in text
    )
