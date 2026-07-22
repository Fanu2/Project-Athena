"""
Chunking adapter factory.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.adapter import (
    ChunkingAdapter,
)

from athena.indexing.chunking_engine.legacy_adapter import (
    LegacyChunkingAdapter,
)

from athena.indexing.chunking_engine.settings import (
    ChunkingSettings,
)

from athena.indexing.chunking_engine.structure_adapter import (
    StructureChunkingAdapter,
)


class ChunkingAdapterFactory:
    """
    Creates chunking adapters from settings.
    """

    @staticmethod
    def create(
        settings: ChunkingSettings | None = None,
    ) -> ChunkingAdapter:
        """
        Create configured chunking adapter.
        """

        settings = settings or ChunkingSettings()

        if settings.engine == "structure":
            return StructureChunkingAdapter()

        return LegacyChunkingAdapter()