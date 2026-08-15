"""
Athena plugin interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from athena.plugins.models import PluginInfo


class AthenaPlugin(ABC):
    """
    Base contract for Athena plugins.
    """

    @property
    @abstractmethod
    def info(
        self,
    ) -> PluginInfo:
        """
        Return plugin metadata.
        """
        raise NotImplementedError

    def initialize(
        self,
        context,
    ) -> None:
        """
        Initialize plugin.

        Plugins may override this.
        """

    def shutdown(
        self,
    ) -> None:
        """
        Shutdown plugin.

        Plugins may override this.
        """
