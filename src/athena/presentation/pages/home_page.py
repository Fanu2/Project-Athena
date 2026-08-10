"""
Home page.

Displays Athena workspace overview
and workspace intelligence summary.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.workspace.intelligence.models import (
    WorkspaceIntelligenceSnapshot,
)

from athena.workspace.models import Workspace


class HomePage(QWidget):
    """
    Application home page.

    Shows current workspace state and
    workspace intelligence information.
    """

    def __init__(self) -> None:
        super().__init__()

        self.title_label = QLabel(
            "Welcome to Athena"
        )

        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.workspace_label = QLabel(
            "No workspace is currently open."
        )

        self.workspace_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.path_label = QLabel()

        self.path_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.intelligence_label = QLabel()

        self.intelligence_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout = QVBoxLayout(self)

        layout.addStretch()

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.workspace_label
        )

        layout.addWidget(
            self.path_label
        )

        layout.addWidget(
            self.intelligence_label
        )

        layout.addStretch()

    def set_workspace(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Display active workspace identity.
        """

        self.title_label.setText(
            "Workspace"
        )

        self.workspace_label.setText(
            workspace.name
        )

        self.path_label.setText(
            str(workspace.path)
        )

    def set_workspace_intelligence(
        self,
        snapshot: WorkspaceIntelligenceSnapshot,
    ) -> None:
        """
        Display workspace intelligence summary.
        """

        self.title_label.setText(
            "Workspace Intelligence"
        )

        self.workspace_label.setText(
            snapshot.workspace_name
        )

        self.intelligence_label.setText(
            "\n".join(
                [
                    (
                        f"Documents: "
                        f"{snapshot.document_count}"
                    ),
                    (
                        f"Pages: "
                        f"{snapshot.page_count}"
                    ),
                    (
                        f"Knowledge Items: "
                        f"{snapshot.knowledge_item_count}"
                    ),
                    (
                        f"Conversation Messages: "
                        f"{snapshot.conversation_messages}"
                    ),
                ]
            )
        )

    def clear_workspace(self) -> None:
        """
        Reset page state.
        """

        self.title_label.setText(
            "Welcome to Athena"
        )

        self.workspace_label.setText(
            "No workspace is currently open."
        )

        self.path_label.clear()

        self.intelligence_label.clear()