"""
AI Settings page.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from athena.ai.llm.provider import LLMProvider
from athena.ai.providers.provider_health_service import (
    ProviderHealthService,
)

from athena.settings import (
    AISettings,
    AISettingsService,
)

from athena.presentation.settings.model_info_widget import (
    ModelInfoWidget,
)

from athena.presentation.settings.provider_status_widget import (
    ProviderStatusWidget,
)

from athena.presentation.settings.routing_explanation_widget import (
    RoutingExplanationWidget,
)

from athena.presentation.settings.routing_policy_widget import (
    RoutingPolicyWidget,
)


class AISettingsPage(QWidget):
    """Workspace AI Control Center page."""

    def __init__(
        self,
        provider: LLMProvider | None = None,
        health_service: ProviderHealthService | None = None,
    ) -> None:
        """Initialize AI settings page."""

        super().__init__()

        if provider is None:
            raise RuntimeError(
                "AI provider must be supplied."
            )

        self._provider = provider

        self._health_service = (
            health_service
            if health_service is not None
            else ProviderHealthService()
        )

        self._settings_service: (
            AISettingsService | None
        ) = None

        self._create_ui()

        self._load_models()

        self._refresh_provider_status()

        self._update_model_information()

    def set_settings_service(
        self,
        service: AISettingsService,
    ) -> None:
        """Attach workspace AI settings service."""

        self._settings_service = service

        self._load_settings()

    def _create_ui(self) -> None:
        """Create user interface."""

        layout = QVBoxLayout(
            self,
        )

        title = QLabel(
            "AI Control Center",
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignLeft,
        )

        layout.addWidget(
            title,
        )

        form = QFormLayout()

        self.model_combo = QComboBox()

        form.addRow(
            "Default Model:",
            self.model_combo,
        )

        layout.addLayout(
            form,
        )

        self.model_info = ModelInfoWidget()

        layout.addWidget(
            self.model_info,
        )

        self.routing_explanation = (
            RoutingExplanationWidget()
        )

        layout.addWidget(
            self.routing_explanation,
        )

        self.routing_policy = (
            RoutingPolicyWidget()
        )

        layout.addWidget(
            self.routing_policy,
        )

        self.provider_status = (
            ProviderStatusWidget()
        )

        layout.addWidget(
            self.provider_status,
        )

        button_layout = QHBoxLayout()

        self.refresh_button = QPushButton(
            "Refresh Models",
        )

        self.save_button = QPushButton(
            "Save",
        )

        self.cancel_button = QPushButton(
            "Cancel",
        )

        button_layout.addWidget(
            self.refresh_button,
        )

        button_layout.addStretch()

        button_layout.addWidget(
            self.save_button,
        )

        button_layout.addWidget(
            self.cancel_button,
        )

        layout.addLayout(
            button_layout,
        )

        layout.addStretch()

        self.save_button.clicked.connect(
            self._save_settings,
        )

        self.cancel_button.clicked.connect(
            self._cancel_changes,
        )

        self.refresh_button.clicked.connect(
            self._refresh_models,
        )

        self.model_combo.currentTextChanged.connect(
            self._update_model_information,
        )

    def _load_models(self) -> None:
        """Load available provider models."""

        self.model_combo.clear()

        try:
            models = sorted(
                self._provider.list_models(),
            )

            self.model_combo.addItems(
                models,
            )

        except Exception:
            self.model_combo.addItem(
                "No models available",
            )

    def _get_selected_model(self):
        """Return selected model information."""

        model_name = (
            self.model_combo.currentText()
        )

        try:
            if hasattr(
                self._provider,
                "get_model",
            ):
                return self._provider.get_model(
                    model_name,
                )

        except Exception:
            return None

        return None

    def _update_model_information(
        self,
    ) -> None:
        """Update selected model details."""

        model = self._get_selected_model()

        self.model_info.update_model(
            model,
        )

        self.routing_explanation.update_model(
            model,
        )

    def _refresh_provider_status(
        self,
    ) -> None:
        """Refresh provider health."""

        health = []

        try:
            provider_name = getattr(
                self._provider,
                "provider_name",
                "unknown",
            )

            health.append(
                self._health_service.check_provider(
                    provider_id=provider_name,
                )
            )

        except Exception:
            pass

        self.provider_status.update_health(
            health,
        )

    def _load_settings(self) -> None:
        """Load workspace AI settings."""

        if self._settings_service is None:
            return

        settings = (
            self._settings_service.load()
        )

        index = self.model_combo.findText(
            settings.default_model,
        )

        if index >= 0:
            self.model_combo.setCurrentIndex(
                index,
            )

        if hasattr(
            settings,
            "routing_policy",
        ):
            self.routing_policy.set_policy(
                settings.routing_policy,
            )

    def _save_settings(self) -> None:
        """Save workspace AI settings."""

        if self._settings_service is None:
            return

        settings = AISettings(
            default_model=(
                self.model_combo.currentText()
            ),
        )

        if hasattr(
            settings,
            "routing_policy",
        ):
            settings.routing_policy = (
                self.routing_policy.selected_policy()
            )

        self._settings_service.save(
            settings,
        )

    def _cancel_changes(self) -> None:
        """Discard unsaved changes."""

        self._load_settings()

    def _refresh_models(self) -> None:
        """Refresh available provider models."""

        current_model = (
            self.model_combo.currentText()
        )

        self._load_models()

        index = self.model_combo.findText(
            current_model,
        )

        if index >= 0:
            self.model_combo.setCurrentIndex(
                index,
            )

        self._update_model_information()

        self._refresh_provider_status()