"""
Workspace statistics widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)


class WorkspaceStatistics(
    QFrame,
):
    """
    Displays workspace intelligence statistics.
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

        self.documents_label = QLabel(
            "0",
        )

        self.pages_label = QLabel(
            "0",
        )

        self.knowledge_label = QLabel(
            "0",
        )

        self.evidence_label = QLabel(
            "0",
        )

        self.citation_label = QLabel(
            "0",
        )

        self.conversation_label = QLabel(
            "0",
        )

        self._setup_ui()


    def _setup_ui(
        self,
    ) -> None:
        """
        Create statistics card.
        """

        layout = QVBoxLayout(
            self,
        )

        title = QLabel(
            "📊 Workspace Intelligence",
        )

        title.setStyleSheet(
            "font-weight: bold; font-size: 14px;"
        )

        layout.addWidget(
            title,
        )

        self._add_metric(
            layout,
            "Documents",
            self.documents_label,
        )

        self._add_metric(
            layout,
            "Pages",
            self.pages_label,
        )

        self._add_metric(
            layout,
            "Knowledge Items",
            self.knowledge_label,
        )

        self._add_metric(
            layout,
            "Evidence Records",
            self.evidence_label,
        )

        self._add_metric(
            layout,
            "Citations",
            self.citation_label,
        )

        self._add_metric(
            layout,
            "Conversation Messages",
            self.conversation_label,
        )


    def _add_metric(
        self,
        layout: QVBoxLayout,
        name: str,
        value: QLabel,
    ) -> None:
        """
        Add metric row.
        """

        label = QLabel(
            name,
        )

        value.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        layout.addWidget(
            label,
        )

        layout.addWidget(
            value,
        )


    def set_snapshot(
        self,
        snapshot: WorkspaceIntelligenceSnapshot,
    ) -> None:
        """
        Display workspace statistics.
        """

        self.documents_label.setText(
            str(snapshot.document_count),
        )

        self.pages_label.setText(
            str(snapshot.page_count),
        )

        self.knowledge_label.setText(
            str(snapshot.knowledge_item_count),
        )

        self.evidence_label.setText(
            str(snapshot.evidence_count),
        )

        self.citation_label.setText(
            str(snapshot.citation_count),
        )

        self.conversation_label.setText(
            str(snapshot.conversation_messages),
        )


    def clear(
        self,
    ) -> None:
        """
        Reset statistics.
        """

        self.documents_label.setText(
            "0",
        )

        self.pages_label.setText(
            "0",
        )

        self.knowledge_label.setText(
            "0",
        )

        self.evidence_label.setText(
            "0",
        )

        self.citation_label.setText(
            "0",
        )

        self.conversation_label.setText(
            "0",
        )
