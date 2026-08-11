"""
Tests for assistant execution request creation.
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

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)


def test_engine_creates_execution_request():

    engine = AssistantEngine(
        IntentService(),
    )

    plan = AssistantPlan(
        capability="summary",
        steps=(
            "generate_response",
        ),
    )

    request = engine.create_execution_request(
        plan,
    )

    assert request.plan == plan
