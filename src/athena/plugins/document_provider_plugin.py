"""
Document provider plugin contract.

Allows plugins to provide knowledge acquisition providers.
"""

from __future__ import annotations

from abc import abstractmethod

from athena.knowledge.acquisition.contracts.provider import (
    Provider,
)

from athena.plugins.base import (
    AthenaPlugin,
)


class DocumentProviderPlugin(AthenaPlugin):
    """
    Plugin capable of providing
    knowledge acquisition providers.
    """

    @abstractmethod
    def create_provider(
        self,
    ) -> Provider:
        """
        Create a knowledge provider.
        """

        raise NotImplementedError
