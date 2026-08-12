"""
Tests for controlled assistant execution boundary.
"""

from athena.application.assistant.executor import (
    DisabledAssistantExecutor,
)

from athena.application.assistant.execution import (
    AssistantExecutionRequest,
)


def test_disabled_executor_blocks_execution():

    executor = DisabledAssistantExecutor()

    request = AssistantExecutionRequest(
        plan=None,
    )

    result = executor.execute(
        request,
    )

    assert result.success is False

    assert (
        "not enabled"
        in result.message
    )
