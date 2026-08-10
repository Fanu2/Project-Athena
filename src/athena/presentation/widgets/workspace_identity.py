"""
Workspace identity widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.workspace.models import Workspace


class WorkspaceIdentity(
    QFrame,
):
    """
    Displays workspace identity information.
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


        self.name_label = QLabel(
            "No workspace",
        )

        self.path_label = QLabel(
            "-",
        )

        self.version_label = QLabel(
            "-",
        )


        self._setup_ui()



    def _setup_ui(
        self,
    ) -> None:
        """
        Create identity card.
        """

        layout = QVBoxLayout(
            self,
        )

        title = QLabel(
            "📁 Workspace",
        )

        title.setStyleSheet(
            "font-weight: bold; font-size: 14px;"
        )


        self.name_label.setStyleSheet(
            "font-size: 16px; font-weight: bold;"
        )


        self.path_label.setWordWrap(
            True,
        )


        layout.addWidget(
            title,
        )

        layout.addWidget(
            self.name_label,
        )

        layout.addWidget(
            QLabel("Location"),
        )

        layout.addWidget(
            self.path_label,
        )

        layout.addWidget(
            QLabel("Version"),
        )

        layout.addWidget(
            self.version_label,
        )



    def set_workspace(
        self,
        workspace: Workspace,
    ) -> None:
        """
        Display workspace information.
        """

        self.name_label.setText(
            workspace.name,
        )

        self.path_label.setText(
            str(
                workspace.path,
            ),
        )

        self.version_label.setText(
            workspace.version,
        )



    def clear(
        self,
    ) -> None:
        """
        Reset widget.
        """

        self.name_label.setText(
            "No workspace",
        )

        self.path_label.setText(
            "-",
        )

        self.version_label.setText(
            "-",
        )