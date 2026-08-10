"""
Workspace Intelligence ApplicationContext integration tests.
"""

from pathlib import Path

from athena.core.application_context import (
    ApplicationContext,
)


def test_application_context_creates_workspace_intelligence(
    tmp_path: Path,
):
    context = ApplicationContext()

    workspace = context.workspace_service.create_workspace(
        tmp_path,
        "Research",
    )

    context.open_workspace(
        workspace.path,
    )

    assert (
        context.workspace_intelligence_service
        is not None
    )

    snapshot = (
        context.workspace_intelligence_service.snapshot(
            context.current_workspace,
        )
    )

    assert snapshot.workspace_name == "Research"
    assert (
        snapshot.workspace_id
        == context.current_workspace.workspace_id
    )
