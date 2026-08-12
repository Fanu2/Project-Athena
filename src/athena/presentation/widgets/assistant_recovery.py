"""
Assistant recovery widget.

Displays available assistant sessions.
"""

from __future__ import annotations

from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QListWidget,
    QFrame,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from athena.application.assistant.session import (
    AssistantSession,
)


class AssistantRecoveryWidget(QFrame):
    """
    User-controlled assistant session recovery.
    """

    restore_requested = Signal(
        str,
    )


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

        self.sessions = QListWidget(
            self,
        )

        self.restore_button = QPushButton(
            "Restore Selected",
            self,
        )

        self.restore_button.clicked.connect(
            self._restore_selected,
        )

        self._items: list[
            AssistantSession
        ] = []

        self._setup_ui()


    def _setup_ui(
        self,
    ) -> None:
        """
        Create recovery layout.
        """

        layout = QVBoxLayout(
            self,
        )

        layout.addWidget(
            self.sessions,
        )

        layout.addWidget(
            self.restore_button,
        )


    def set_sessions(
        self,
        sessions: tuple[
            AssistantSession,
            ...
        ],
    ) -> None:
        """
        Display available sessions.
        """

        self._items = list(
            sessions,
        )

        self.sessions.clear()

        for session in sessions:

            self.sessions.addItem(
                (
                    f"{session.workspace_name} "
                    f"- {session.conversation_id}"
                )
            )


    def _restore_selected(
        self,
    ) -> None:
        """
        Emit selected session.
        """

        index = (
            self.sessions.currentRow()
        )

        if index < 0:
            return

        session = self._items[index]

        self.restore_requested.emit(
            session.session_id,
        )
