"""
Athena Provider Registry

Discovers and resolves capability providers.
"""

from typing import Dict

from ..contracts.provider import Provider


class ProviderRegistry:
    """
    Registry for Athena capability providers.
    """

    def __init__(self) -> None:
        self._providers: Dict[str, Provider] = {}

    def register(
        self,
        provider: Provider,
    ) -> None:
        """
        Register provider capabilities.
        """

        for capability in provider.capabilities:
            self._providers[capability] = provider

    def get_provider(
        self,
        capability: str,
    ) -> Provider | None:
        """
        Resolve provider by capability.
        """

        return self._providers.get(capability)

    def capabilities(self) -> list[str]:
        """
        Return available capabilities.
        """

        return list(self._providers.keys())