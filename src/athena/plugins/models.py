"""
Plugin metadata models.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PluginInfo:
    """
    Describes an Athena plugin.
    """

    name: str
    version: str
    description: str = ""
    capabilities: tuple[str, ...] = ()
