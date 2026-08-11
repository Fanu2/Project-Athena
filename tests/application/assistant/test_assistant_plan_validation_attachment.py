"""
Tests for attaching validation diagnostics to plans.
"""

from athena.ai.intent.service import (
    IntentService,
)

from athena.application.assistant.engine import (
    AssistantEngine,
)

from athena.application.assistant.plan import (
    AssistantPlan,
)


def test_engine_attaches_validation_to_plan():

    engine = AssistantEngine(
        IntentService(),
    )

    plan = AssistantPlan(
        capability="summary",
        steps=(
            "generate_response",
        ),
        context_notes=(
            "Workspace: Research",
        ),
    )

    validated_plan = (
        engine.attach_validation(
            plan,
        )
    )

    assert (
        validated_plan.validation
        is not None
    )

    assert (
        validated_plan.validation.valid
        is True
    )

    assert (
        "workflow_present"
        in validated_plan.validation.checks
    )
