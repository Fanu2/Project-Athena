"""
Tests for workspace health intelligence.
"""

from uuid import uuid4

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from athena.workspace.intelligence.health_service import (
    WorkspaceHealthService,
)


def test_empty_workspace_health():

    snapshot = WorkspaceIntelligenceSnapshot(
        workspace_id=uuid4(),
        workspace_name="Empty",
    )

    report = WorkspaceHealthService().evaluate(
        snapshot,
    )

    assert report.documents_ready is False
    assert report.evidence_ready is False
    assert report.retrieval_ready is False


def test_ready_workspace_health():

    snapshot = WorkspaceIntelligenceSnapshot(
        workspace_id=uuid4(),
        workspace_name="Research",
        document_count=10,
        indexed_document_count=10,
        knowledge_item_count=20,
        evidence_count=100,
        citation_count=50,
    )

    report = WorkspaceHealthService().evaluate(
        snapshot,
    )

    assert report.documents_ready is True
    assert report.knowledge_ready is True
    assert report.evidence_ready is True
    assert report.citation_ready is True
    assert report.retrieval_ready is True
