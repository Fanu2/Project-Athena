"""
Workspace intelligence health service.
"""

from __future__ import annotations

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from athena.workspace.intelligence.health import (
    WorkspaceHealthReport,
)


class WorkspaceHealthService:
    """
    Calculates workspace readiness signals.
    """

    def evaluate(
        self,
        snapshot: WorkspaceIntelligenceSnapshot,
    ) -> WorkspaceHealthReport:
        """
        Evaluate workspace health.
        """

        return WorkspaceHealthReport(
            documents_ready=(
                snapshot.document_count > 0
            ),

            knowledge_ready=(
                snapshot.knowledge_item_count > 0
            ),

            evidence_ready=(
                snapshot.evidence_count > 0
            ),

            citation_ready=(
                snapshot.citation_count > 0
            ),

            retrieval_ready=(
                snapshot.indexed_document_count > 0
            ),

            ai_ready=True,
        )
