"""
Routing policy widget.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QGroupBox,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


class RoutingPolicyWidget(QWidget):
    """Allow selection of runtime routing policy."""

    POLICIES = (
        "Balanced",
        "Local First",
        "Reasoning Priority",
        "Fast Response",
    )

    def __init__(
        self,
    ) -> None:
        """Initialize policy widget."""

        super().__init__()

        group = QGroupBox(
            "Routing Policy",
        )

        layout = QVBoxLayout(
            group,
        )

        self.buttons: dict[
            str,
            QRadioButton,
        ] = {}

        for policy in self.POLICIES:
            button = QRadioButton(
                policy,
            )

            layout.addWidget(
                button,
            )

            self.buttons[policy] = button

        self.buttons[
            "Balanced"
        ].setChecked(
            True,
        )

        main_layout = QVBoxLayout(
            self,
        )

        main_layout.addWidget(
            group,
        )

    def selected_policy(
        self,
    ) -> str:
        """Return selected policy."""

        for name, button in (
            self.buttons.items()
        ):
            if button.isChecked():
                return name

        return "Balanced"

    def set_policy(
        self,
        policy: str,
    ) -> None:
        """Set selected policy."""

        button = self.buttons.get(
            policy,
        )

        if button is not None:
            button.setChecked(
                True,
            )