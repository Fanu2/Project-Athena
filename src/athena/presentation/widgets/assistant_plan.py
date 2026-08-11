"""
Assistant plan widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.application.assistant.plan import (
    AssistantPlan,
)


class AssistantPlanWidget(QFrame):
    """
    Displays Athena's planned workflow.
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
            "Athena Plan: -",
        )

        self.content.setWordWrap(
            True,
        )

        self._setup_ui()


    def _setup_ui(
        self,
    ) -> None:
        """
        Create plan card.
        """

        layout = QVBoxLayout(
            self,
        )

        title = QLabel(
            "🧠 Athena Plan",
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


    def set_plan(
        self,
        plan: AssistantPlan,
    ) -> None:
        """
        Display assistant plan.
        """

        lines: list[str] = []

        if plan.context_notes:
            lines.append(
                "Context:"
            )

            lines.extend(
                plan.context_notes,
            )

            lines.append(
                "",
            )

        lines.extend(
            [
                f"Capability: {plan.capability}",
                "",
                "Steps:",
            ]
        )

        for index, step in enumerate(
            plan.steps,
            start=1,
        ):
            lines.append(
                f"{index}. {step.replace('_', ' ')}"
            )

        self.content.setText(
            "\n".join(lines),
        )


    def clear(
        self,
    ) -> None:
        """
        Reset plan display.
        """

        self.content.setText(
            "Athena Plan: -",
        )