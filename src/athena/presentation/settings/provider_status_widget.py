"""
Provider status widget for AI Control Center.
"""

from __future__ import annotations

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from athena.ai.providers.provider_health import (
    ProviderHealth,
)
from athena.ai.providers.provider_health_service import (
    ProviderHealthService,
)


class ProviderStatusWidget(QWidget):
    """Display AI provider health status."""

    def __init__(
        self,
        health_service: ProviderHealthService | None = None,
    ) -> None:
        """Initialize widget."""

        super().__init__()

        self._health_service = (
            health_service
            if health_service is not None
            else ProviderHealthService()
        )

        self._layout = QVBoxLayout(
            self,
        )

        self.title = QLabel(
            "Provider Status"
        )

        self._layout.addWidget(
            self.title,
        )

        self.status_label = QLabel()

        self._layout.addWidget(
            self.status_label,
        )

    def update_health(
        self,
        health: list[ProviderHealth],
    ) -> None:
        """Update displayed provider health."""

        if not health:
            self.status_label.setText(
                "No providers available."
            )
            return

        lines = []

        for provider in health:
            lines.append(
                (
                    f"{provider.provider_id}: "
                    f"{provider.status.value}"
                )
            )

        self.status_label.setText(
            "\n".join(lines)
        )