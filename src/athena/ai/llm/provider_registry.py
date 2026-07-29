"""
Provider registry for Athena LLM providers.
"""

from __future__ import annotations

from athena.ai.llm.provider import LLMProvider


class ProviderRegistry:
    """Registry of available LLM providers."""

    def __init__(self) -> None:
        """Initialize an empty registry."""

        self._providers: dict[str, LLMProvider] = {}
        self._default: str | None = None

    def register(
        self,
        provider: LLMProvider,
    ) -> None:
        """Register a provider."""

        name = provider.provider_name

        if name in self._providers:
            raise ValueError(
                f"Provider '{name}' is already registered."
            )

        self._providers[name] = provider

        if self._default is None:
            self._default = name

    def unregister(
        self,
        name: str,
    ) -> None:
        """Unregister a provider."""

        if name not in self._providers:
            raise KeyError(name)

        del self._providers[name]

        if self._default == name:
            if self._providers:
                self._default = sorted(
                    self._providers.keys()
                )[0]
            else:
                self._default = None

    def get(
        self,
        name: str,
    ) -> LLMProvider:
        """Return a registered provider."""

        return self._providers[name]

    def exists(
        self,
        name: str,
    ) -> bool:
        """Return whether provider exists."""

        return name in self._providers

    def names(self) -> list[str]:
        """Return provider names."""

        return sorted(self._providers.keys())

    def providers(self) -> list[LLMProvider]:
        """Return registered providers."""

        return [
            self._providers[name]
            for name in self.names()
        ]

    def set_default(
        self,
        name: str,
    ) -> None:
        """Set default provider."""

        if name not in self._providers:
            raise KeyError(name)

        self._default = name

    def default(self) -> LLMProvider:
        """Return default provider."""

        if self._default is None:
            raise RuntimeError(
                "No default provider configured."
            )

        return self._providers[self._default]

