"""
Tests for Athena Calibre Provider.
"""

import sqlite3
from pathlib import Path

from athena.knowledge.acquisition.providers.calibre_provider import (
    CalibreProvider,
)


def create_test_calibre_library(
    path: Path,
) -> None:
    """
    Create minimal Calibre library fixture.
    """

    path.mkdir()

    with sqlite3.connect(
        path / "metadata.db"
    ) as connection:

        cursor = connection.cursor()

        cursor.executescript(
            """
            CREATE TABLE books (
                id INTEGER PRIMARY KEY,
                title TEXT,
                path TEXT,
                uuid TEXT,
                has_cover INTEGER
            );

            CREATE TABLE authors (
                id INTEGER PRIMARY KEY,
                name TEXT
            );

            CREATE TABLE books_authors_link (
                book INTEGER,
                author INTEGER
            );

            CREATE TABLE tags (
                id INTEGER PRIMARY KEY,
                name TEXT
            );

            CREATE TABLE books_tags_link (
                book INTEGER,
                tag INTEGER
            );

            CREATE TABLE data (
                book INTEGER,
                format TEXT,
                name TEXT
            );
            """
        )

        cursor.execute(
            """
            INSERT INTO books
            VALUES (
                1,
                'Around the World in 28 Languages',
                'book_folder',
                'test-uuid',
                0
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO authors
            VALUES (
                1,
                'Infogrid Pacific'
            )
            """
        )

        cursor.execute(
            """
            INSERT INTO books_authors_link
            VALUES (1, 1)
            """
        )

        cursor.execute(
            """
            INSERT INTO data
            VALUES (
                1,
                'EPUB',
                'Around the World in 28 Languages'
            )
            """
        )


def test_calibre_provider_library_scan(
    tmp_path: Path,
) -> None:

    library = tmp_path / "Calibre-Test-Library"

    create_test_calibre_library(
        library,
    )

    provider = CalibreProvider()

    books = provider.execute(
        "library_scan",
        library,
    )

    assert len(books) == 1

    assert (
        books[0]["title"]
        == "Around the World in 28 Languages"
    )


def test_calibre_provider_creates_book_artifact(
    tmp_path: Path,
) -> None:

    library = tmp_path / "Calibre-Test-Library"

    create_test_calibre_library(
        library,
    )

    provider = CalibreProvider()

    artifact = provider.execute(
        "book_metadata_import",
        {
            "library_path": str(library),
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
