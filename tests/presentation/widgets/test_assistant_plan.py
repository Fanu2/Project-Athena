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
    )

    widget.set_plan(
        plan,
    )

    assert (
        "summary"
        in widget.content.text()
    )

    assert (
        "retrieve information"
        in widget.content.text()
    )
