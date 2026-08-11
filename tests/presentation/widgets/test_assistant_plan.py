"""
Tests for Assistant Plan widget.
"""

from athena.application.assistant.plan import (
    AssistantPlan,
)

from athena.application.assistant.workflow import (
    AssistantWorkflowStep,
)

from athena.presentation.widgets.assistant_plan import (
    AssistantPlanWidget,
)


def test_plan_widget_displays_plan(
    qtbot,
):
    """
    Widget displays capability,
    context, and workflow.
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
        ),
        workflow_steps=(
            AssistantWorkflowStep(
                name="retrieve_information",
                description=(
                    "Search workspace documents"
                ),
                category="retrieval",
            ),
            AssistantWorkflowStep(
                name="attach_citations",
                description=(
                    "Attach source references"
                ),
                category="citation",
            ),
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
        "Context:"
        in text
    )

    assert (
        "Workspace: Research"
        in text
    )

    assert (
        "Workflow:"
        in text
    )

    assert (
        "retrieve information"
        in text
    )

    assert (
        "Search workspace documents"
        in text
    )

    assert (
        "attach citations"
        in text
    )
