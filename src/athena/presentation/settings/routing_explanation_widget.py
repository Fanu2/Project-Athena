"""
Routing explanation widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.ai.llm.model_info import ModelInfo
from athena.ai.llm.model_scorer import (
    ModelScoringService,
)


class RoutingExplanationWidget(QWidget):
    """Display why a model was selected."""

    def __init__(
        self,
        scorer: ModelScoringService | None = None,
    ) -> None:
        """Initialize widget."""

        super().__init__()

        self._scorer = (
            scorer
            if scorer is not None
            else ModelScoringService()
        )

        layout = QVBoxLayout(
            self,
        )

        self.title = QLabel(
            "Routing Explanation",
        )

        layout.addWidget(
            self.title,
        )

        self.details = QLabel()

        self.details.setWordWrap(
            True,
        )

        layout.addWidget(
            self.details,
        )

    def update_model(
        self,
        model: ModelInfo | None,
    ) -> None:
        """Update routing explanation."""

        if model is None:
            self.details.setText(
                "No active model."
            )
            return

        score = self._scorer.score(
            model,
        )

        reasons = []

        if model.capabilities.chat:
            reasons.append(
                "✓ Chat capable"
            )

        if model.capabilities.reasoning:
            reasons.append(
                "✓ Reasoning capable"
            )

        if model.capabilities.local:
            reasons.append(
                "✓ Local model"
            )

        if score.health_score > 0:
            reasons.append(
                "✓ Runtime history available"
            )

        reasons.append(
            f"✓ Routing score: "
            f"{score.total:.1f}"
        )

        self.details.setText(
            "\n".join(reasons),
        )