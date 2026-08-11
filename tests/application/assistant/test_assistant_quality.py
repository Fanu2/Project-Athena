"""
Tests for assistant quality service.
"""

from athena.application.assistant.plan import (
    AssistantPlan,
)

from athena.application.assistant.quality import (
    AssistantQualityService,
)


def test_quality_service_validates_plan():

    service = AssistantQualityService()

    plan = AssistantPlan(
        capability="summary",
        steps=(
            "generate_response",
        ),
        context_notes=(
            "Workspace: Research",
        ),
    )

    result = service.validate(
        plan,
    )

    assert result.valid is True

    assert (
        "capability_available"
        in result.checks
    )

    assert (
        "workflow_present"
        in result.checks
    )
