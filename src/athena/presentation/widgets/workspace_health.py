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
        *,
        documents: bool,
        knowledge: bool,
        retrieval: bool,
        conversation: bool,
        runtime: bool,
    ) -> None:
        """
        Update health indicators.
        """

        self.documents_status.setText(
            self._format(
                "Documents",
                documents,
            )
        )

        self.knowledge_status.setText(
            self._format(
                "Knowledge",
                knowledge,
            )
        )

        self.retrieval_status.setText(
            self._format(
                "Retrieval",
                retrieval,
            )
        )

        self.conversation_status.setText(
            self._format(
                "Conversation",
                conversation,
            )
        )

        self.runtime_status.setText(
            self._format(
                "AI Runtime",
                runtime,
            )
        )


    def clear(self) -> None:
        """
        Reset health state.
        """

        self.update_health(
            documents=False,
            knowledge=False,
            retrieval=False,
            conversation=False,
            runtime=False,
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
