"""
Storage for workspace AI settings.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import AISettings


class AISettingsStorage:
    """Reads and writes workspace AI settings."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> AISettings:
        """Load workspace AI settings."""

        if not self._path.exists():
            return AISettings()

        with self._path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        return AISettings(
            default_model=data.get(
                "default_model",
                AISettings().default_model,
            ),
        )

    def save(
        self,
        settings: AISettings,
    ) -> None:
        """Save workspace AI settings."""

        self._path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with self._path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                {
                    "default_model": settings.default_model,
                },
                file,
                indent=4,
            )