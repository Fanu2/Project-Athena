"""
Tests for Assistant Context integration.
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


def test_assistant_engine_uses_workspace_context():
    """
    Assistant decisions should be created
    with workspace intelligence available.
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
        workspace_name="Research",
        document_count=10,
        knowledge_item_count=10,
    )

    engine = AssistantEngine(
        IntentService(),
    )

    decision = engine.analyze_request(
        "Explain this document",
        snapshot,
    )

    assert decision.capability.name == "explanation"

    assert decision.confidence >= 0.0
