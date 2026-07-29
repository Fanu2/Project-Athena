"""
OpenAI provider.
"""

from __future__ import annotations

from athena.ai.llm.providers.openai_compatible import (
    OpenAICompatibleProvider,
)
from athena.settings import LLMSettings


class OpenAIProvider(OpenAICompatibleProvider):
    """OpenAI provider."""

    DEFAULT_SETTINGS = LLMSettings(
        provider="openai",
        model="gpt-5",
        base_url="https://api.openai.com",
    )

    def __init__(
        self,
        settings: LLMSettings | None = None,
    ) -> None:
        super().__init__(settings or self.DEFAULT_SETTINGS)

    @property
    def provider_name(self) -> str:
        return "openai"

    def validate_configuration(self) -> None:
        super().validate_configuration()

        if not self._settings.api_key.strip():
            raise ValueError(
                "OpenAI requires an API key."
            )
