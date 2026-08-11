"""
Tests for Assistant Plan widget.
"""

from athena.application.assistant.plan import (
    AssistantPlan,
)

from athena.presentation.widgets.assistant_plan import (
    AssistantPlanWidget,
)


def test_plan_widget_displays_plan(
    qtbot,
):
    """
    Widget displays capability, steps,
    and workspace context.
    """

    widget = AssistantPlanWidget()

    qtbot.addWidget(
        widget,
    )

    plan = AssistantPlan(
        capability="summary",
        steps=(
            "retrieve_information",
            "attach_citations",
        ),
        context_notes=(
            "Workspace: Research",
            "Documents available: 10",
            "Knowledge items: 5",
        ),
    )

    widget.set_plan(
        plan,
    )

    text = widget.content.text()

    assert (
        "summary"
        in text
    )

    assert (
        "retrieve information"
        in text
    )

    assert (
        "Workspace: Research"
        in text
    )

    assert (
        "Documents available: 10"
        in text
    )

    assert (
        "Knowledge items: 5"
        in text
    )
