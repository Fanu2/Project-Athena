"""
Workspace awareness tests.
"""

from uuid import uuid4

from athena.application.assistant.workspace_awareness import (
    WorkspaceAwareness,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from athena.workspace.intelligence.health import (
    WorkspaceHealthReport,
)


def test_workspace_summary():

    snapshot = WorkspaceIntelligenceSnapshot(
        workspace_id=uuid4(),
        workspace_name="Test Workspace",
        document_count=10,
        indexed_document_count=8,
        knowledge_item_count=5,
        evidence_count=4,
        citation_count=3,
    )

    result = (
        WorkspaceAwareness()
        .summary(snapshot)
    )

    assert "Test Workspace" in result
    assert "Documents: 10" in result
    assert "Citations: 3" in result


def test_workspace_health():

    report = WorkspaceHealthReport(
        documents_ready=True,
        knowledge_ready=True,
        evidence_ready=False,
        citation_ready=True,
        retrieval_ready=True,
        ai_ready=True,
    )

    result = (
        WorkspaceAwareness()
        .health(report)
    )

    assert "Documents: ready" in result
    assert "Evidence: not ready" in result


def test_workspace_activity():

    snapshot = WorkspaceIntelligenceSnapshot(
        workspace_id=uuid4(),
        workspace_name="Test Workspace",
        recent_documents=(
            "a.pdf",
            "b.pdf",
        ),
        recent_queries=(
            "query",
        ),
        recent_sessions=(
            "session",
            "session2",
        ),
    )

    result = (
        WorkspaceAwareness()
        .activity(snapshot)
    )

    assert "Recent documents: 2" in result
    assert "Recent queries: 1" in result
    assert "Recent sessions: 2" in result
