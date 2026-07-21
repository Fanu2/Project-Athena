"""
Athena application settings compatibility layer.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from athena.settings.llm_settings import LLMSettings


@dataclass(slots=True)
class AISettings:
    """Backward compatible AI settings."""

    default_model: str = "gemma3:4b"


class AISettingsService:
    """Workspace AI settings storage."""

    def __init__(
        self,
        path: Path,
    ) -> None:
        self._path = path

    def load(self) -> AISettings:
        """Load AI settings."""

        if not self._path.exists():
            return AISettings()

        data = json.loads(
            self._path.read_text(
                encoding="utf-8",
            )
        )

        return AISettings(
            default_model=data.get(
                "default_model",
                "gemma3:4b",
            ),
        )

    def save(
        self,
        settings: AISettings,
    ) -> None:
        """Save AI settings."""

        self._path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._path.write_text(
            json.dumps(
                {
                    "default_model": settings.default_model,
                },
                indent=4,
            ),
            encoding="utf-8",
        )


__all__ = [
    "LLMSettings",
    "AISettings",
    "AISettingsService",
]
