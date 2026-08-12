"""
Assistant memory widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.application.assistant.memory import (
    AssistantMemoryItem,
)


class AssistantMemoryWidget(QFrame):
    """
    Displays approved assistant memories.
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
            "Assistant Memory: -",
        )

        self.content.setWordWrap(
            True,
        )

        self._setup_ui()


    def _setup_ui(
        self,
    ) -> None:
        """
        Create memory card.
        """

        layout = QVBoxLayout(
            self,
        )

        title = QLabel(
            "🧠 Assistant Memory",
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


    def set_memories(
        self,
        memories: tuple[
            AssistantMemoryItem,
            ...,
        ],
    ) -> None:
        """
        Display approved memories.
        """

        if not memories:
            self.content.setText(
                "No memories stored.",
            )
            return

        lines = []

        for memory in memories:
            lines.extend(
                [
                    f"Key: {memory.key}",
                    f"Value: {memory.value}",
                    f"Scope: {memory.scope}",
                    f"Source: {memory.source}",
                    "",
                ]
            )

        self.content.setText(
            "\n".join(
                lines,
            )
        )


    def clear(
        self,
    ) -> None:
        """
        Reset memory display.
        """

        self.content.setText(
            "Assistant Memory: -",
        )
