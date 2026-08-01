"""
Athena SQLite Evidence Repository

Persistent storage for EvidenceRecord.
"""

from __future__ import annotations

import json
import sqlite3
import threading

from uuid import UUID

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)


class SQLiteEvidenceRepository:
    """
    SQLite implementation of evidence storage.

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
                CREATE TABLE IF NOT EXISTS evidence_records (
                    evidence_id TEXT PRIMARY KEY,
                    source_id TEXT,
                    source_reference TEXT,
                    location TEXT,
                    extraction_method TEXT,
                    provider TEXT,
                    confidence REAL,
                    metadata TEXT
                )
                """
            )

            self._connection.commit()

    def save(
        self,
        evidence: EvidenceRecord,
    ) -> None:
        """
        Persist evidence record.
        """

        print(
            "EVIDENCE SAVE:",
            evidence.source_reference,
            "DB:",
            self._database_path,
        )

        with self._lock:

            self._connection.execute(
                """
                INSERT OR REPLACE INTO evidence_records
                (
                    evidence_id,
                    source_id,
                    source_reference,
                    location,
                    extraction_method,
                    provider,
                    confidence,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(
                        evidence.evidence_id
                    ),
                    (
                        str(evidence.source_id)
                        if evidence.source_id
                        else None
                    ),
                    evidence.source_reference,
                    evidence.location,
                    evidence.extraction_method,
                    evidence.provider,
                    evidence.confidence,
                    json.dumps(
                        evidence.metadata
                    ),
                ),
            )

            self._connection.commit()

        print(
            "EVIDENCE SAVED:",
            evidence.evidence_id,
        )

    def list_all(
        self,
    ) -> list[EvidenceRecord]:
        """
        Return all evidence records.
        """

        with self._lock:

            rows = (
                self._connection
                .execute(
                    """
                    SELECT
                        evidence_id,
                        source_id,
                        source_reference,
                        location,
                        extraction_method,
                        provider,
                        confidence,
                        metadata
                    FROM evidence_records
                    """
                )
                .fetchall()
            )

        return [
            self._row_to_record(row)
            for row in rows
        ]

    def find_by_object(
        self,
        object_id: UUID,
    ) -> list[EvidenceRecord]:
        """
        Find evidence by knowledge object.
        """

        with self._lock:

            rows = (
                self._connection
                .execute(
                    """
                    SELECT
                        evidence_id,
                        source_id,
                        source_reference,
                        location,
                        extraction_method,
                        provider,
                        confidence,
                        metadata
                    FROM evidence_records
                    WHERE source_id = ?
                    """,
                    (
                        str(object_id),
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
    ) -> EvidenceRecord:
        """
        Convert SQLite row into EvidenceRecord.
        """

        return EvidenceRecord(
            evidence_id=UUID(row[0]),
            source_id=(
                UUID(row[1])
                if row[1]
                else None
            ),
            source_reference=row[2],
            location=row[3],
            extraction_method=row[4],
            provider=row[5],
            confidence=row[6],
            metadata=(
                json.loads(row[7])
                if row[7]
                else {}
            ),
        )