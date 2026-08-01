"""
Athena SQLite Citation Repository

Persistent storage for CitationRecord.
"""

from __future__ import annotations

import json
import sqlite3
import threading

from uuid import UUID

from athena.knowledge.acquisition.domain.citation_record import (
    CitationRecord,
)


class SQLiteCitationRepository:
    """
    SQLite implementation of citation storage.

    Thread-safe for background import workers.
    """

    def __init__(
        self,
        database_path: str,
    ) -> None:

        self._database_path = database_path

        self._lock = threading.Lock()

        self._connection = sqlite3.connect(
            database_path,
            check_same_thread=False,
        )

        self._create_table()

    def _create_table(
        self,
    ) -> None:

        with self._lock:

            self._connection.execute(
                """
                CREATE TABLE IF NOT EXISTS citation_records (
                    citation_id TEXT PRIMARY KEY,
                    evidence_id TEXT,
                    source_reference TEXT,
                    citation_text TEXT,
                    location TEXT,
                    confidence REAL,
                    metadata TEXT
                )
                """
            )

            self._connection.commit()

    def save(
        self,
        citation: CitationRecord,
    ) -> None:
        """
        Persist citation record.
        """

        print(
            "CITATION SAVE:",
            citation.source_reference,
            "DB:",
            self._database_path,
        )

        with self._lock:

            self._connection.execute(
                """
                INSERT OR REPLACE INTO citation_records
                (
                    citation_id,
                    evidence_id,
                    source_reference,
                    citation_text,
                    location,
                    confidence,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(
                        citation.citation_id
                    ),
                    (
                        str(citation.evidence_id)
                        if citation.evidence_id
                        else None
                    ),
                    citation.source_reference,
                    citation.citation_text,
                    citation.location,
                    citation.confidence,
                    json.dumps(
                        citation.metadata
                    ),
                ),
            )

            self._connection.commit()

        print(
            "CITATION SAVED:",
            citation.citation_id,
        )

    def list_all(
        self,
    ) -> list[CitationRecord]:
        """
        Return all citations.
        """

        with self._lock:

            rows = (
                self._connection
                .execute(
                    """
                    SELECT
                        citation_id,
                        evidence_id,
                        source_reference,
                        citation_text,
                        location,
                        confidence,
                        metadata
                    FROM citation_records
                    """
                )
                .fetchall()
            )

        return [
            self._row_to_record(row)
            for row in rows
        ]

    def find_by_evidence(
        self,
        evidence_id: UUID,
    ) -> list[CitationRecord]:
        """
        Find citations linked to evidence.
        """

        with self._lock:

            rows = (
                self._connection
                .execute(
                    """
                    SELECT
                        citation_id,
                        evidence_id,
                        source_reference,
                        citation_text,
                        location,
                        confidence,
                        metadata
                    FROM citation_records
                    WHERE evidence_id = ?
                    """,
                    (
                        str(evidence_id),
                    ),
                )
                .fetchall()
            )

        return [
            self._row_to_record(row)
            for row in rows
        ]

    def _row_to_record(
        self,
        row,
    ) -> CitationRecord:
        """
        Convert SQLite row into CitationRecord.
        """

        return CitationRecord(
            citation_id=UUID(row[0]),
            evidence_id=(
                UUID(row[1])
                if row[1]
                else None
            ),
            source_reference=row[2],
            citation_text=row[3],
            location=row[4],
            confidence=row[5],
            metadata=(
                json.loads(row[6])
                if row[6]
                else {}
            ),
        )