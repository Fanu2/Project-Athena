"""
OpenAI provider.
"""

from __future__ import annotations

from athena.ai.llm.metadata import ProviderMetadata
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

    @property
    def metadata(self) -> ProviderMetadata:
        """Return provider metadata."""

        return ProviderMetadata(
            name="openai",
            display_name="OpenAI",
            local=False,
            requires_api_key=True,
            supports_chat=True,
            supports_streaming=True,
            supports_tools=True,
            supports_vision=True,
        )

    def validate_configuration(self) -> None:
        super().validate_configuration()

        if not self._settings.api_key.strip():
            raise ValueError(
                "OpenAI requires an API key."
            )
