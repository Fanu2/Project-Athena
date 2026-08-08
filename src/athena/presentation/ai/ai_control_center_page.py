"""
AI Control Center page.

Displays Athena AI runtime information.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.core.application_context import ApplicationContext


class AIControlCenterPage(QWidget):
    """Manage Athena AI runtime."""

    def __init__(
        self,
        context: ApplicationContext,
        parent: QWidget | None = None,
    ) -> None:
        """Initialize AI Control Center."""

        super().__init__(parent)

        self._context = context

        self._layout = QVBoxLayout(self)

        self._title = QLabel(
            "AI Control Center",
        )

        self._layout.addWidget(
            self._title,
        )

        self._models_label = QLabel()

        self._layout.addWidget(
            self._models_label,
        )

        self.refresh()

    def refresh(self) -> None:
        """Refresh AI runtime information."""

        manager = self._context.model_manager

        if manager is None:
            self._models_label.setText(
                "Model Manager unavailable\n"
                "Open a workspace to initialize AI runtime."
            )
            return

        lines = [
            "Installed Models",
            "",
        ]

        for model in manager.models():

            capabilities = []

            if model.capabilities.chat:
                capabilities.append(
                    "chat",
                )

            if model.capabilities.streaming:
                capabilities.append(
                    "streaming",
                )

            if model.capabilities.tools:
                capabilities.append(
                    "tools",
                )

            if model.capabilities.vision:
                capabilities.append(
                    "vision",
                )

            if model.capabilities.embeddings:
                capabilities.append(
                    "embedding",
                )

            if model.capabilities.reasoning:
                capabilities.append(
                    "reasoning",
                )

            if model.capabilities.reranking:
                capabilities.append(
                    "reranking",
                )

            lines.extend(
                [
                    model.name,
                    f"Provider: {model.provider}",
                    (
                        "Capabilities: "
                        + (
                            ", ".join(capabilities)
                            if capabilities
                            else "none"
                        )
                    ),
                    "",
                ]
            )

        self._models_label.setText(
            "\n".join(lines),
        )