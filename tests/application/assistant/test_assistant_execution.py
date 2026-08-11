"""
Tests for assistant execution boundary models.
"""

from athena.application.assistant.execution import (
    AssistantExecutionRequest,
    AssistantExecutionResult,
)

from athena.application.assistant.plan import (
    AssistantPlan,
)


def test_execution_request_wraps_plan():

    plan = AssistantPlan(
        capability="summary",
        steps=(
            "generate_response",
        ),
    )

    request = AssistantExecutionRequest(
        plan=plan,
    )

    assert request.plan == plan


def test_execution_result_contains_status():

    result = AssistantExecutionResult(
        success=False,
        message="Execution not available",
    )

    assert result.success is False

    assert (
        result.message
        == "Execution not available"
    )
