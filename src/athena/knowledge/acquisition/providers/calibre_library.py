"""
Athena Calibre Library Reader

Reads book metadata from a Calibre library.
"""

import sqlite3
from pathlib import Path


class CalibreLibraryReader:
    """
    Reads a Calibre metadata.db file.
    """

    def __init__(
        self,
        library_path: Path,
    ) -> None:

        self.library_path = Path(library_path)

        self.database_path = (
            self.library_path / "metadata.db"
        )

    def exists(self) -> bool:
        """
        Check whether this is a valid Calibre library.
        """

        return self.database_path.exists()

    def list_books(self) -> list[dict]:
        """
        Return books available in the Calibre library.
        """

        if not self.exists():
            raise FileNotFoundError(
                "Calibre metadata.db not found"
            )

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    path,
                    uuid
                FROM books
                ORDER BY title
                """
            )

            rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "title": row[1],
                "path": row[2],
                "uuid": row[3],
            }
            for row in rows
        ]

    def get_book(
        self,
        book_id: int,
    ) -> dict:
        """
        Return detailed metadata for one book.
        """

        if not self.exists():
            raise FileNotFoundError(
                "Calibre metadata.db not found"
            )

        with sqlite3.connect(
            self.database_path
        ) as connection:

            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    title,
                    path,
                    uuid,
                    has_cover
                FROM books
                WHERE id = ?
                """,
                (book_id,),
            )

            book = cursor.fetchone()

            if book is None:
                raise ValueError(
                    f"Book not found: {book_id}"
                )

            metadata = {
                "id": book["id"],
                "title": book["title"],
                "path": book["path"],
                "uuid": book["uuid"],
                "has_cover": bool(book["has_cover"]),
                "authors": [],
                "tags": [],
                "formats": [],
                "series": None,
            }

            cursor.execute(
                """
                SELECT authors.name
                FROM authors
                JOIN books_authors_link
                    ON authors.id = books_authors_link.author
                WHERE books_authors_link.book = ?
                """,
                (book_id,),
            )

            metadata["authors"] = [
                row["name"]
                for row in cursor.fetchall()
            ]

            cursor.execute(
                """
                SELECT tags.name
                FROM tags
                JOIN books_tags_link
                    ON tags.id = books_tags_link.tag
                WHERE books_tags_link.book = ?
                """,
                (book_id,),
            )

            metadata["tags"] = [
                row["name"]
                for row in cursor.fetchall()
            ]

            cursor.execute(
                """
                SELECT format
                FROM data
                WHERE book = ?
                """,
                (book_id,),
            )

            metadata["formats"] = [
                row["format"]
                for row in cursor.fetchall()
            ]

        return metadata

    def get_book_file(
        self,
        book_id: int,
        book_format: str = "EPUB",
    ) -> Path:
        """
        Return the actual book file path
        from Calibre metadata.
        """

        if not self.exists():
            raise FileNotFoundError(
                "Calibre metadata.db not found"
            )

        with sqlite3.connect(
            self.database_path
        ) as connection:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    books.path,
                    data.name
                FROM books
                JOIN data
                    ON books.id = data.book
                WHERE books.id = ?
                AND data.format = ?
                """,
                (
                    book_id,
                    book_format.upper(),
                ),
            )

            row = cursor.fetchone()

            if row is None:
                raise ValueError(
                    f"No {book_format} file found for book {book_id}"
                )

        return (
            self.library_path
            / row[0]
            / f"{row[1]}.{book_format.lower()}"
        )