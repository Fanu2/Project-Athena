"""
Tests for Assistant planning.
"""

from pathlib import Path
from datetime import datetime

from athena.ai.intent.service import (
    IntentService,
)

from athena.application.assistant.engine import (
    AssistantEngine,
)

from athena.workspace.models import (
    Workspace,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)


def snapshot():
    workspace = Workspace(
        name="Research",
        path=Path("/tmp/research"),
        version="1.0",
        created=datetime.now(),
        modified=datetime.now(),
    )

    return WorkspaceIntelligenceSnapshot(
        workspace_id=workspace.workspace_id,
        workspace_name=workspace.name,
    )


def test_summary_request_creates_plan():

    engine = AssistantEngine(
        IntentService(),
    )

    decision = engine.analyze_request(
        "Summarize my documents with sources",
        snapshot(),
    )

    plan = engine.create_plan(
        decision,
    )

    assert plan.capability == "summary"

    assert (
        "retrieve_information"
        in plan.steps
    )

    assert (
        "attach_citations"
        in plan.steps
    )
