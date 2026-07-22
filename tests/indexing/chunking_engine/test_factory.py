"""
Tests for ChunkingAdapterFactory.
"""

from __future__ import annotations

from athena.indexing.chunking_engine.factory import (
    ChunkingAdapterFactory,
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


def test_default_factory_returns_legacy_adapter():
    """Default configuration should preserve old behavior."""

    adapter = ChunkingAdapterFactory.create()

    assert isinstance(
        adapter,
        LegacyChunkingAdapter,
    )


def test_legacy_setting_returns_legacy_adapter():
    """Explicit legacy mode should use legacy chunking."""

    settings = ChunkingSettings(
        engine="legacy",
    )

    adapter = ChunkingAdapterFactory.create(
        settings,
    )

    assert isinstance(
        adapter,
        LegacyChunkingAdapter,
    )


def test_structure_setting_returns_structure_adapter():
    """Structure mode should use new chunking engine."""

    settings = ChunkingSettings(
        engine="structure",
    )

    adapter = ChunkingAdapterFactory.create(
        settings,
    )

    assert isinstance(
        adapter,
        StructureChunkingAdapter,
    )


def test_unknown_setting_falls_back_to_legacy():
    """Unknown values should not break indexing."""

    settings = ChunkingSettings(
        engine="unknown",
    )

    adapter = ChunkingAdapterFactory.create(
        settings,
    )

    assert isinstance(
        adapter,
        LegacyChunkingAdapter,
    )