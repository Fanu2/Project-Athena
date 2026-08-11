"""
Tests for Assistant capability routing.
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


def create_snapshot():
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
        document_count=5,
        knowledge_item_count=5,
    )


def test_summary_routes_to_evidence_capable_workflow():
    engine = AssistantEngine(
        IntentService(),
    )

    decision = engine.analyze_request(
        "Summarize my documents",
        create_snapshot(),
    )

    assert decision.capability.name == "summary"

    assert (
        decision.capability.requires_retrieval
        is True
    )

    assert (
        decision.capability.requires_evidence
        is True
    )

    assert (
        decision.capability.requires_citations
        is True
    )


def test_search_routes_to_retrieval():
    engine = AssistantEngine(
        IntentService(),
    )

    decision = engine.analyze_request(
        "Search for this document",
        create_snapshot(),
    )

    assert decision.capability.name == "retrieval"

    assert (
        decision.capability.requires_retrieval
        is True
    )
