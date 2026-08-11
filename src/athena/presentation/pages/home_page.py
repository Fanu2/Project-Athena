"""
Home page.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.workspace.models import Workspace

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from athena.workspace.intelligence.health import (
    WorkspaceHealthReport,
)

from athena.presentation.widgets.workspace_identity import (
    WorkspaceIdentity,
)

from athena.presentation.widgets.workspace_statistics import (
    WorkspaceStatistics,
)

from athena.presentation.widgets.workspace_health import (
    WorkspaceHealth,
)


class HomePage(QWidget):
    """
    Athena workspace dashboard.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(
            parent,
        )

        #
        # Header
        #

        self.title_label = QLabel(
            "Welcome to Athena",
        )

        self.title_label.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            """
        )

        self.subtitle_label = QLabel(
            "Personal offline AI workspace",
        )

        #
        # Dashboard widgets
        #

        self.workspace_identity = (
            WorkspaceIdentity()
        )

        self.workspace_statistics = (
            WorkspaceStatistics()
        )

        self.workspace_health = (
            WorkspaceHealth()
        )

        self._setup_ui()


    def _setup_ui(
        self,
    ) -> None:
        """
        Build dashboard layout.
        """

        layout = QVBoxLayout(
            self,
        )

        layout.addWidget(
            self.title_label,
        )

        layout.addWidget(
            self.subtitle_label,
        )

        cards = QHBoxLayout()

        cards.addWidget(
            self.workspace_identity,
        )

        cards.addWidget(
            self.workspace_statistics,
        )

        cards.addWidget(
            self.workspace_health,
        )

        layout.addLayout(
            cards,
        )

        layout.addStretch()


    def set_workspace(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Display active workspace.
        """

        self.title_label.setText(
            "Workspace Dashboard",
        )

        self.subtitle_label.setText(
            "Athena workspace intelligence",
        )

        self.workspace_identity.set_workspace(
            workspace,
        )


    def set_workspace_snapshot(
        self,
        snapshot: WorkspaceIntelligenceSnapshot,
    ) -> None:
        """
        Display workspace intelligence snapshot.
        """

        self.workspace_statistics.set_snapshot(
            snapshot,
        )


    def set_workspace_health(
        self,
        report: WorkspaceHealthReport,
    ) -> None:
        """
        Update workspace health status.
        """

        self.workspace_health.update_health(
            report,
        )


    def clear_workspace(
        self,
    ) -> None:
        """
        Reset dashboard.
        """

        self.title_label.setText(
            "Welcome to Athena",
        )

        self.subtitle_label.setText(
            "Personal offline AI workspace",
        )

        self.workspace_identity.clear()

        self.workspace_statistics.clear()

        self.workspace_health.clear()
