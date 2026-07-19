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

from athena.ai.llm.ollama import OllamaProvider
from athena.settings import (
    AISettings,
    AISettingsService,
)


class AISettingsPage(QWidget):
    """Workspace AI settings page."""

    def __init__(
        self,
        provider: OllamaProvider | None = None,
    ) -> None:
        """Initialize the AI Settings page."""

        super().__init__()

        self._provider = provider or OllamaProvider()
        self._settings_service: AISettingsService | None = None

        self._create_ui()
        self._load_models()

    def set_settings_service(
        self,
        service: AISettingsService,
    ) -> None:
        """Attach the workspace AI settings service."""

        self._settings_service = service
        self._load_settings()

    def _create_ui(self) -> None:
        """Create the user interface."""

        layout = QVBoxLayout(self)

        title = QLabel("AI Settings")
        title.setAlignment(
            Qt.AlignmentFlag.AlignLeft,
        )

        layout.addWidget(title)

        form = QFormLayout()

        self.model_combo = QComboBox()

        form.addRow(
            "Default Model:",
            self.model_combo,
        )

        layout.addLayout(form)

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

        self.save_button.clicked.connect(
            self._save_settings,
        )

        self.cancel_button.clicked.connect(
            self._cancel_changes,
        )

        self.refresh_button.clicked.connect(
            self._refresh_models,
        )

        self.save_button.clicked.connect(
            self._save_settings,
        )

        self.cancel_button.clicked.connect(
            self._cancel_changes,
        )

    def _load_models(self) -> None:
        """Load installed Ollama models."""

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

    def _load_settings(self) -> None:
        """Load workspace AI settings."""

        if self._settings_service is None:
            return

        settings = self._settings_service.load()

        index = self.model_combo.findText(
            settings.default_model,
        )

        if index >= 0:
            self.model_combo.setCurrentIndex(
                index,
            )

    def _save_settings(self) -> None:
        """Save workspace AI settings."""

        if self._settings_service is None:
            return

        settings = AISettings(
            default_model=self.model_combo.currentText(),
        )

        self._settings_service.save(
            settings,
        )

    def _cancel_changes(self) -> None:
        """Discard unsaved changes."""

        self._load_settings()

    def _refresh_models(self) -> None:
        """Refresh installed Ollama models."""

        current_model = self.model_combo.currentText()

        self._load_models()

        index = self.model_combo.findText(
            current_model,
        )

        if index >= 0:
            self.model_combo.setCurrentIndex(
                index,
            )