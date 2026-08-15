"""
Tests for Athena Calibre Provider.
"""

from pathlib import Path

from athena.knowledge.acquisition.providers.calibre_provider import (
    CalibreProvider,
)


def test_calibre_provider_library_scan():

    provider = CalibreProvider()

    books = provider.execute(
        "library_scan",
        Path.home() / "Calibre-Test-Library",
    )

    assert len(books) == 1

    assert (
        books[0]["title"]
        == "Around the World in 28 Languages"
    )


def test_calibre_provider_creates_book_artifact():

    provider = CalibreProvider()

    artifact = provider.execute(
        "book_metadata_import",
        {
            "library_path": str(
                Path.home()
                / "Calibre-Test-Library"
            ),
            "book_id": 1,
        },
    )

    assert artifact.artifact_type == "book"

    assert (
        artifact.metadata["title"]
        == "Around the World in 28 Languages"
    )

    assert (
        artifact.metadata["authors"]
        == ["Infogrid Pacific"]
    )

    assert (
        artifact.metadata["formats"]
        == ["EPUB"]
    )

    assert (
        artifact.metadata["provider"]
        == "calibre"
    )
