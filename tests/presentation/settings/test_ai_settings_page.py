"""
Tests for AI Settings Page.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock

import pytest

from PySide6.QtWidgets import QApplication

from athena.ai.llm.capabilities import (
    ModelCapabilities,
)

from athena.ai.llm.model_info import (
    ModelInfo,
)

from athena.presentation.settings.ai_settings_page import (
    AISettingsPage,
)

from athena.settings import (
    AISettingsService,
)


@pytest.fixture
def app():
    """Provide Qt application."""

    application = QApplication.instance()

    if application is None:
        application = QApplication([])

    return application


def create_provider() -> Mock:
    """Create mock provider."""

    provider = Mock()

    provider.provider_name = (
        "ollama"
    )

    models = {
        "qwen3:4b": ModelInfo(
            name="qwen3:4b",
            provider="ollama",
            context_window=8192,
            capabilities=ModelCapabilities(
                chat=True,
                reasoning=True,
                local=True,
            ),
        ),
        "llava": ModelInfo(
            name="llava",
            provider="ollama",
            context_window=8192,
            capabilities=ModelCapabilities(
                vision=True,
                local=True,
            ),
        ),
    }

    provider.list_models.return_value = list(
        models.keys(),
    )

    provider.get_model.side_effect = (
        lambda name: models.get(name)
    )

    return provider


def test_ai_settings_page_loads_models(
    app,
) -> None:
    """Page loads provider models."""

    page = AISettingsPage(
        provider=create_provider(),
    )

    assert (
        page.model_combo.count()
        == 2
    )


def test_ai_control_center_widgets_exist(
    app,
) -> None:
    """Control center widgets exist."""

    page = AISettingsPage(
        provider=create_provider(),
    )

    assert (
        page.model_info
        is not None
    )

    assert (
        page.routing_explanation
        is not None
    )

    assert (
        page.routing_policy
        is not None
    )

    assert (
        page.provider_status
        is not None
    )


def test_ai_settings_persistence(
    app,
    tmp_path: Path,
) -> None:
    """Settings are persisted."""

    page = AISettingsPage(
        provider=create_provider(),
    )

    service = AISettingsService(
        tmp_path / "ai.json",
    )

    page.set_settings_service(
        service,
    )

    page.model_combo.setCurrentText(
        "llava",
    )

    page.routing_policy.set_policy(
        "Reasoning Priority",
    )

    page._save_settings()

    loaded = service.load()

    assert (
        loaded.default_model
        == "llava"
    )

    assert (
        loaded.routing_policy
        == "Reasoning Priority"
    )