"""
Athena Provider Manager

Controls provider discovery and execution.
"""

from typing import Any

from ..contracts.provider import Provider
from ..registry.provider_registry import ProviderRegistry


class ProviderManager:
    """
    Manages Athena capability providers.
    """

    def __init__(
        self,
        registry: ProviderRegistry | None = None,
    ) -> None:

        self.registry = (
            registry
            if registry is not None
            else ProviderRegistry()
        )

    def register(
        self,
        provider: Provider,
    ) -> None:
        """
        Register provider.
        """

        self.registry.register(provider)

    def execute(
        self,
        capability: str,
        input_data: Any,
    ) -> Any:
        """
        Execute capability provider.
        """

        provider = self.registry.get_provider(
            capability
        )

        if provider is None:
            raise ValueError(
                f"No provider found for capability: {capability}"
            )

        return provider.execute(
            capability,
            input_data,
        )