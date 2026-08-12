"""
Workspace activity widget.
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


class WorkspaceActivity(
    QFrame,
):
    """
    Displays workspace activity context.
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
            "Recent Documents: -",
        )

        self.queries_label = QLabel(
            "Recent Queries: -",
        )

        self.sessions_label = QLabel(
            "Recent Sessions: -",
        )

        self._setup_ui()


    def _setup_ui(
        self,
    ) -> None:
        """
        Create activity card.
        """

        layout = QVBoxLayout(
            self,
        )

        title = QLabel(
            "🕒 Workspace Activity",
        )

        title.setStyleSheet(
            "font-weight: bold; font-size: 14px;"
        )

        layout.addWidget(
            title,
        )

        layout.addWidget(
            self.documents_label,
        )

        layout.addWidget(
            self.queries_label,
        )

        layout.addWidget(
            self.sessions_label,
        )


    def set_snapshot(
        self,
        snapshot: WorkspaceIntelligenceSnapshot,
    ) -> None:
        """
        Display workspace activity.
        """

        self.documents_label.setText(
            "Recent Documents:\n"
            + "\n".join(
                snapshot.recent_documents
            )
            if snapshot.recent_documents
            else "Recent Documents: -",
        )

        self.queries_label.setText(
            "Recent Queries:\n"
            + "\n".join(
                snapshot.recent_queries
            )
            if snapshot.recent_queries
            else "Recent Queries: -",
        )

        self.sessions_label.setText(
            "Recent Sessions:\n"
            + "\n".join(
                snapshot.recent_sessions
            )
            if snapshot.recent_sessions
            else "Recent Sessions: -",
        )


    def clear(
        self,
    ) -> None:
        """
        Reset activity.
        """

        self.documents_label.setText(
            "Recent Documents: -",
        )

        self.queries_label.setText(
            "Recent Queries: -",
        )

        self.sessions_label.setText(
            "Recent Sessions: -",
        )
