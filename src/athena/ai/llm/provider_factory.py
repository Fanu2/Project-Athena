"""
Provider factory for Athena LLM providers.
"""

from __future__ import annotations

from athena.ai.llm.provider import LLMProvider
from athena.ai.llm.providers import (
    LMStudioProvider,
    OpenAIProvider,
    OllamaProvider,
)
from athena.settings import LLMSettings


class ProviderFactory:
    """Factory for creating LLM providers."""

    def create(
        self,
        provider_name: str | None = None,
        settings: LLMSettings | None = None,
    ) -> LLMProvider:
        """Create a provider."""

        settings = (
            settings
            if settings is not None
            else LLMSettings()
        )

        name = (
            provider_name
            if provider_name is not None
            else settings.provider
        ).lower()

        if name == "ollama":
            return OllamaProvider(settings)

        if name == "lmstudio":
            return LMStudioProvider(settings)

        if name == "openai":
            return OpenAIProvider(settings)

        raise ValueError(
            f"Unknown provider: {name}"
        )

    def supported_providers(self) -> list[str]:
        """Return supported providers."""

        return [
            "ollama",
            "lmstudio",
            "openai",
        ]
