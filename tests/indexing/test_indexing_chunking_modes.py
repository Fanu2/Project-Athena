"""
Tests for IndexingService chunking mode selection.
"""

from __future__ import annotations

import pytest

from athena.indexing.chunking_engine.legacy_adapter import (
    LegacyChunkingAdapter,
)

from athena.indexing.chunking_engine.settings import (
    ChunkingSettings,
)

from athena.indexing.chunking_engine.structure_adapter import (
    StructureChunkingAdapter,
)

from athena.indexing.repositories.memory import (
    MemoryChunkRepository,
)

from athena.indexing.service import (
    IndexingService,
)


@pytest.fixture
def memory_repository():
    """
    Provide in-memory chunk repository.
    """

    return MemoryChunkRepository()


def test_default_indexing_service_uses_legacy_chunking(
    memory_repository,
):
    """
    Default indexing should preserve legacy behavior.
    """

    service = IndexingService(
        repository=memory_repository,
    )

    assert isinstance(
        service._chunking,
        LegacyChunkingAdapter,
    )


def test_structure_mode_selects_structure_adapter(
    memory_repository,
):
    """
    Structure mode should activate the new engine.
    """

    service = IndexingService(
        repository=memory_repository,
        chunking_settings=ChunkingSettings(
            engine="structure",
        ),
    )

    assert isinstance(
        service._chunking,
        StructureChunkingAdapter,
    )


def test_explicit_adapter_overrides_settings(
    memory_repository,
):
    """
    Injected adapter should take priority over settings.
    """

    adapter = LegacyChunkingAdapter()

    service = IndexingService(
        repository=memory_repository,
        chunking_adapter=adapter,
        chunking_settings=ChunkingSettings(
            engine="structure",
        ),
    )

    assert service._chunking is adapter