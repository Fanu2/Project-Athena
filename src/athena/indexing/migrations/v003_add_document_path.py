"""
Add document path to chunks.

Allows citation navigation from retrieved
evidence back to the original document.
"""

from __future__ import annotations

import sqlite3

from athena.indexing.migrations.migration import (
    Migration,
)


class V003AddDocumentPath(Migration):
    """Add document_path column to chunks."""

    version = 3

    def apply(
        self,
        connection: sqlite3.Connection,
    ) -> None:
        """Apply migration."""

        connection.execute(
            """
            ALTER TABLE chunks
            ADD COLUMN document_path TEXT
            """
        )