"""
Assistant session widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.application.assistant.session import (
    AssistantSession,
)


class AssistantSessionWidget(QFrame):
    """
    Displays active assistant session state.
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

        self.content = QLabel(
            "Assistant Session: -",
        )

        self.content.setWordWrap(
            True,
        )

        self._setup_ui()


    def _setup_ui(
        self,
    ) -> None:
        """
        Create session card.
        """

        layout = QVBoxLayout(
            self,
        )

        title = QLabel(
            "🧠 Assistant Session",
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
            self.content,
        )


    def set_session(
        self,
        session: AssistantSession,
    ) -> None:
        """
        Display assistant session.
        """

        self.content.setText(
            "\n".join(
                [
                    (
                        f"Workspace: "
                        f"{session.workspace_name}"
                    ),
                    (
                        f"Conversation: "
                        f"{session.conversation_id}"
                    ),
                    (
                        f"Created: "
                        f"{session.created_at}"
                    ),
                ]
            )
        )


    def clear(
        self,
    ) -> None:
        """
        Reset session display.
        """

        self.content.setText(
            "Assistant Session: -",
        )
