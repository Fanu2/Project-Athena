"""
Model information widget for AI Control Center.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.ai.llm.model_info import ModelInfo


class ModelInfoWidget(QWidget):
    """Display selected model information."""

    def __init__(
        self,
    ) -> None:
        """Initialize widget."""

        super().__init__()

        self._layout = QVBoxLayout(
            self,
        )

        self.title = QLabel(
            "Model Information",
        )

        self._layout.addWidget(
            self.title,
        )

        self.details = QLabel()

        self.details.setWordWrap(
            True,
        )

        self._layout.addWidget(
            self.details,
        )

    def update_model(
        self,
        model: ModelInfo | None,
    ) -> None:
        """Display model details."""

        if model is None:
            self.details.setText(
                "No model selected."
            )
            return

        capabilities = []

        if model.capabilities.chat:
            capabilities.append(
                "Chat"
            )

        if model.capabilities.reasoning:
            capabilities.append(
                "Reasoning"
            )

        if model.capabilities.vision:
            capabilities.append(
                "Vision"
            )

        if model.capabilities.embeddings:
            capabilities.append(
                "Embeddings"
            )

        if model.capabilities.tools:
            capabilities.append(
                "Tools"
            )

        if model.capabilities.local:
            capabilities.append(
                "Local"
            )

        text = (
            f"Model: {model.name}\n"
            f"Provider: {model.provider}\n"
            f"Context: "
            f"{model.context_window}\n"
            f"Capabilities: "
            f"{', '.join(capabilities)}"
        )

        self.details.setText(
            text,
        )