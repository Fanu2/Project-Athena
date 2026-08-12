from uuid import uuid4

from athena.presentation.pages.home_page import (
    HomePage,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from athena.workspace.intelligence.health import (
    WorkspaceHealthReport,
)

def test_home_page_accepts_workspace_intelligence_snapshot(
    qtbot,
):
    page = HomePage()

    qtbot.addWidget(
        page,
    )

    snapshot = WorkspaceIntelligenceSnapshot(
        workspace_id=uuid4(),
        workspace_name="Research",
        document_count=5,
        page_count=20,
        knowledge_item_count=10,
        evidence_count=15,
        citation_count=8,
        recent_documents=(
            "report.pdf",
        ),
        recent_queries=(
            "Find ownership details",
        ),
        recent_sessions=(
            "session-001",
        ),
    )

    page.set_workspace_snapshot(
        snapshot,
    )

    assert (
        page.workspace_statistics.documents_label.text()
        == "5"
    )

    assert (
        page.workspace_activity.documents_label.text()
        != "Recent Documents: -"
    )
