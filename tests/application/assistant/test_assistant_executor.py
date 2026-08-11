"""
Tests for assistant executor boundary.
"""

from athena.application.assistant.execution import (
    AssistantExecutionRequest,
)

from athena.application.assistant.executor import (
    DisabledAssistantExecutor,
)

from athena.application.assistant.plan import (
    AssistantPlan,
)


def test_disabled_executor_does_not_execute():

    plan = AssistantPlan(
        capability="summary",
        steps=(
            "generate_response",
        ),
    )

    request = AssistantExecutionRequest(
        plan=plan,
    )

    executor = DisabledAssistantExecutor()

    result = executor.execute(
        request,
    )

    assert result.success is False

    assert (
        result.message
        == "Assistant execution is not enabled"
    )
