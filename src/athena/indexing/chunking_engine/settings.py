"""
Chunking engine configuration.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ChunkingSettings:
    """
    Configuration for document chunking.

    The default remains legacy to preserve
    existing Athena indexing behavior.
    """

    engine: str = "legacy"