"""
Home page.

Workspace dashboard container.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from athena.workspace.models import Workspace

from athena.presentation.widgets.workspace_identity import (
    WorkspaceIdentity,
)

from athena.presentation.widgets.workspace_statistics import (
    WorkspaceStatistics,
)


class HomePage(QWidget):
    """
    Athena workspace dashboard.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.workspace_identity = (
            WorkspaceIdentity()
        )

        self.workspace_statistics = (
            WorkspaceStatistics()
        )

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Create dashboard layout."""

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.workspace_identity,
        )

        layout.addWidget(
            self.workspace_statistics,
        )

    def set_workspace(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Display workspace identity.
        """

        self.workspace_identity.set_workspace(
            workspace,
        )

    def set_workspace_intelligence(
        self,
        snapshot: WorkspaceIntelligenceSnapshot,
    ) -> None:
        """
        Display workspace statistics.
        """

        self.workspace_statistics.set_snapshot(
            snapshot,
        )

    def clear_workspace(self) -> None:
        """
        Reset dashboard.
        """

        self.workspace_identity.clear()

        self.workspace_statistics.clear()