"""
Provider registry for Athena AI runtimes.
"""

from __future__ import annotations

from athena.ai.providers.provider import Provider


class ProviderRegistry:
    """Registry of available AI providers."""

    def __init__(self) -> None:
        self._providers: dict[str, Provider] = {}

    def register(
        self,
        provider: Provider,
    ) -> None:
        """Register an AI provider."""

        self._providers[
            provider.provider_id
        ] = provider

    def get(
        self,
        provider_id: str,
    ) -> Provider | None:
        """Return provider by id."""

        return self._providers.get(
            provider_id
        )

    def providers(
        self,
    ) -> list[Provider]:
        """Return all providers."""

        return list(
            self._providers.values()
        )

    def enabled_providers(
        self,
    ) -> list[Provider]:
        """Return enabled providers."""

        return [
            provider
            for provider in self._providers.values()
            if provider.enabled
        ]