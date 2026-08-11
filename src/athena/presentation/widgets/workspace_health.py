"""
Workspace health widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.workspace.intelligence.health import (
    WorkspaceHealthReport,
)


class WorkspaceHealth(QFrame):
    """
    Displays workspace readiness status.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(
            parent,
        )

        self.setFrameShape(
            QFrame.Shape.StyledPanel,
        )

        self.documents_status = QLabel(
            "⚠ Documents: Unknown",
        )

        self.knowledge_status = QLabel(
            "⚠ Knowledge: Unknown",
        )

        self.evidence_status = QLabel(
            "⚠ Evidence: Unknown",
        )

        self.citation_status = QLabel(
            "⚠ Citations: Unknown",
        )

        self.retrieval_status = QLabel(
            "⚠ Retrieval: Unknown",
        )

        self.conversation_status = QLabel(
            "⚠ Conversation: Unknown",
        )

        self.runtime_status = QLabel(
            "⚠ AI Runtime: Unknown",
        )

        self._setup_ui()


    def _setup_ui(
        self,
    ) -> None:
        """
        Create health card.
        """

        layout = QVBoxLayout(
            self,
        )

        title = QLabel(
            "🩺 Workspace Health",
        )

        title.setStyleSheet(
            """
            font-weight: bold;
            font-size: 14px;
            """
        )

        layout.addWidget(
            title,
        )

        layout.addWidget(
            self.documents_status,
        )

        layout.addWidget(
            self.knowledge_status,
        )

        layout.addWidget(
            self.evidence_status,
        )

        layout.addWidget(
            self.citation_status,
        )

        layout.addWidget(
            self.retrieval_status,
        )

        layout.addWidget(
            self.conversation_status,
        )

        layout.addWidget(
            self.runtime_status,
        )


    def update_health(
        self,
        report: WorkspaceHealthReport,
    ) -> None:
        """
        Update health indicators.
        """

        self.documents_status.setText(
            self._format(
                "Documents",
                report.documents_ready,
            )
        )

        self.knowledge_status.setText(
            self._format(
                "Knowledge",
                report.knowledge_ready,
            )
        )

        self.evidence_status.setText(
            self._format(
                "Evidence",
                report.evidence_ready,
            )
        )

        self.citation_status.setText(
            self._format(
                "Citations",
                report.citation_ready,
            )
        )

        self.retrieval_status.setText(
            self._format(
                "Retrieval",
                report.retrieval_ready,
            )
        )

        self.conversation_status.setText(
            self._format(
                "Conversation",
                True,
            )
        )

        self.runtime_status.setText(
            self._format(
                "AI Runtime",
                report.ai_ready,
            )
        )


    def clear(
        self,
    ) -> None:
        """
        Reset health state.
        """

        self.update_health(
            WorkspaceHealthReport(),
        )


    def _format(
        self,
        name: str,
        ready: bool,
    ) -> str:
        """
        Format status.
        """

        if ready:
            return f"✓ {name}: Ready"

        return f"⚠ {name}: Not Ready"
