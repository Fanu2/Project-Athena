"""
Workspace awareness helpers for Athena Assistant.
"""

from __future__ import annotations

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from athena.workspace.intelligence.health import (
    WorkspaceHealthReport,
)


class WorkspaceAwareness:
    """
    Formats workspace intelligence for assistant use.
    """

    def summary(
        self,
        snapshot: WorkspaceIntelligenceSnapshot,
    ) -> str:
        """
        Create workspace summary.
        """

        return (
            f"Workspace: {snapshot.workspace_name}\n"
            f"Documents: {snapshot.document_count}\n"
            f"Indexed documents: {snapshot.indexed_document_count}\n"
            f"Knowledge items: {snapshot.knowledge_item_count}\n"
            f"Evidence items: {snapshot.evidence_count}\n"
            f"Citations: {snapshot.citation_count}"
        )

    def health(
        self,
        report: WorkspaceHealthReport,
    ) -> str:
        """
        Create workspace health summary.
        """

        checks = [
            ("Documents", report.documents_ready),
            ("Knowledge", report.knowledge_ready),
            ("Evidence", report.evidence_ready),
            ("Citations", report.citation_ready),
            ("Retrieval", report.retrieval_ready),
            ("AI", report.ai_ready),
        ]

        return "\n".join(
            f"{name}: {'ready' if value else 'not ready'}"
            for name, value in checks
        )

    def activity(
        self,
        snapshot: WorkspaceIntelligenceSnapshot,
    ) -> str:
        """
        Create recent activity summary.
        """

        return (
            f"Recent documents: "
            f"{len(snapshot.recent_documents)}\n"
            f"Recent queries: "
            f"{len(snapshot.recent_queries)}\n"
            f"Recent sessions: "
            f"{len(snapshot.recent_sessions)}"
        )
