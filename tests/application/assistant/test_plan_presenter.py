"""
Tests for assistant plan presentation.
"""

from athena.application.assistant.plan import (
    AssistantPlan,
)

from athena.application.assistant.plan_presenter import (
    AssistantPlanPresenter,
)


def test_plan_presenter_creates_readable_output():

    plan = AssistantPlan(
        capability="summary",
        steps=(
            "retrieve_information",
            "attach_citations",
        ),
    )

    text = AssistantPlanPresenter().present(
        plan,
    )

    assert "Athena Plan" in text

    assert (
        "retrieve information"
        in text
    )

    assert (
        "attach citations"
        in text
    )
