"""
Athena Calibre Metadata Reader

Provides Calibre book metadata extraction.
"""

from pathlib import Path
from typing import Any


class CalibreMetadataReader:
    """
    Reads metadata from a Calibre library.

    Initial implementation provides the
    abstraction boundary for Calibre imports.
    """

    def read_book(
        self,
        book_path: Path,
    ) -> dict[str, Any]:
        """
        Read metadata for a single book.

        Real Calibre metadata.db support
        will be added in the next step.
        """

        return {
            "title": book_path.stem,
            "path": str(book_path),
            "source": "calibre",
        }
