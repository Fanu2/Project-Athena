"""
Tests for Athena Assistant Engine.
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


def test_assistant_engine_detects_summary_request():
    """
    Assistant should route summary requests
    to summary capability.
    """

    workspace = Workspace(
        name="Research",
        path=Path("/tmp/research"),
        version="1.0",
        created=datetime.now(),
        modified=datetime.now(),
    )

    snapshot = WorkspaceIntelligenceSnapshot(
        workspace_id=workspace.workspace_id,
        workspace_name=workspace.name,
        document_count=5,
    )

    engine = AssistantEngine(
        IntentService(),
    )

    decision = engine.analyze_request(
        "Summarize my documents",
        snapshot,
    )

    assert decision.capability.name == "summary"

    assert decision.confidence >= 0.0
