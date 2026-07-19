"""
Service for workspace AI settings.
"""

from __future__ import annotations

from pathlib import Path

from .models import AISettings
from .storage import AISettingsStorage


class AISettingsService:
    """High-level interface for workspace AI settings."""

    def __init__(self, path: Path) -> None:
        self._storage = AISettingsStorage(path)

    def load(self) -> AISettings:
        """Load workspace AI settings."""
        return self._storage.load()

    def save(self, settings: AISettings) -> None:
        """Save workspace AI settings."""
        self._storage.save(settings)