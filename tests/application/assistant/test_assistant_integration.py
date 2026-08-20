"""
Assistant Engine ApplicationContext integration tests.
"""

from pathlib import Path

from athena.core.application_context import (
    ApplicationContext,
)


def test_application_context_creates_assistant_engine(
    tmp_path: Path,
):
    """
    AssistantEngine should be available after
    workspace initialization.
    """

    context = ApplicationContext()

    workspace = (
        context.workspace_service.create_workspace(
            tmp_path,
            "Research",
        )
    )

    context.open_workspace(
        workspace.path,
    )

    assert (
        context.assistant_engine
        is not None
    )

    assert (
        context.assistant_executor
        is not None
    )
