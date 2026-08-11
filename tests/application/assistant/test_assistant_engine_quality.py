"""
Tests for engine plan validation.
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


def test_engine_validates_plan():

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

    result = engine.validate_plan(
        plan,
    )

    assert result.valid is True

    assert (
        "workflow_present"
        in result.checks
    )
