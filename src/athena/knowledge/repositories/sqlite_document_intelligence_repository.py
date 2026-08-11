"""
Athena SQLite Document Intelligence Repository

Persistent storage for DocumentIntelligence.
"""

from __future__ import annotations

import json
import sqlite3
import threading

from datetime import UTC, datetime
from uuid import UUID

from athena.knowledge.intelligence.document_intelligence import (
    DocumentIntelligence,
)

from athena.knowledge.intelligence.document_profile import (
    DocumentProfile,
)

from athena.knowledge.intelligence.document_metadata_profile import (
    DocumentMetadataProfile,
)

from athena.knowledge.intelligence.document_structure import (
    DocumentStructureNode,
)

from athena.knowledge.intelligence.evidence_profile import (
    EvidenceProfile,
)


class SQLiteDocumentIntelligenceRepository:
    """
    SQLite implementation of document intelligence storage.
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
                CREATE TABLE IF NOT EXISTS document_intelligence (
                    document_id TEXT PRIMARY KEY,
                    profile TEXT NOT NULL,
                    metadata TEXT NOT NULL,
                    structure TEXT NOT NULL,
                    evidence TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

            self._connection.commit()


    def save(
        self,
        document_id: str,
        intelligence: DocumentIntelligence,
    ) -> None:
        """
        Persist document intelligence.
        """

        with self._lock:

            self._connection.execute(
                """
                INSERT OR REPLACE INTO document_intelligence
                (
                    document_id,
                    profile,
                    metadata,
                    structure,
                    evidence,
                    created_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    document_id,
                    json.dumps(
                        self._profile_to_dict(
                            intelligence.profile,
                        )
                    ),
                    json.dumps(
                        self._metadata_to_dict(
                            intelligence.metadata,
                        )
                    ),
                    json.dumps(
                        self._structure_to_list(
                            intelligence.structure,
                        )
                    ),
                    json.dumps(
                        self._evidence_to_list(
                            intelligence.evidence,
                        )
                    ),
                    datetime.now(
                        UTC,
                    ).isoformat(),
                ),
            )

            self._connection.commit()


    def get(
        self,
        document_id: str,
    ) -> DocumentIntelligence | None:
        """
        Retrieve document intelligence.
        """

        with self._lock:

            row = (
                self._connection
                .execute(
                    """
                    SELECT
                        profile,
                        metadata,
                        structure,
                        evidence
                    FROM document_intelligence
                    WHERE document_id = ?
                    """,
                    (
                        document_id,
                    ),
                )
                .fetchone()
            )

        if row is None:
            return None


        structure = [
            DocumentStructureNode(
                node_id=UUID(
                    item["node_id"],
                ),
                node_type=item["node_type"],
                title=item["title"],
                level=item["level"],
                parent_id=(
                    UUID(
                        item["parent_id"],
                    )
                    if item["parent_id"]
                    else None
                ),
            )
            for item in json.loads(row[2])
        ]


        evidence = [
            EvidenceProfile(
                evidence_id=UUID(
                    item["evidence_id"],
                ),
                source_document=(
                    UUID(
                        item["source_document"],
                    )
                    if item["source_document"]
                    else None
                ),
                evidence_type=item["evidence_type"],
                content=item["content"],
                location=item["location"],
                confidence=item["confidence"],
                metadata=item["metadata"],
            )
            for item in json.loads(row[3])
        ]


        return DocumentIntelligence(
            profile=DocumentProfile(
                **json.loads(row[0]),
            ),
            metadata=DocumentMetadataProfile(
                **json.loads(row[1]),
            ),
            structure=structure,
            evidence=evidence,
        )


    def _profile_to_dict(
        self,
        profile: DocumentProfile,
    ) -> dict:

        return {
            "title": profile.title,
            "document_type": profile.document_type,
            "page_count": profile.page_count,
            "section_count": profile.section_count,
            "entity_count": profile.entity_count,
            "metadata": profile.metadata,
            "confidence": profile.confidence,
        }


    def _metadata_to_dict(
        self,
        metadata: DocumentMetadataProfile,
    ) -> dict:

        return {
            "document_type": metadata.document_type,
            "language": metadata.language,
            "author": metadata.author,
            "tags": metadata.tags,
            "metadata": metadata.metadata,
            "confidence": metadata.confidence,
        }


    def _structure_to_list(
        self,
        nodes: list[DocumentStructureNode],
    ) -> list[dict]:

        return [
            {
                "node_id": str(node.node_id),
                "node_type": node.node_type,
                "title": node.title,
                "level": node.level,
                "parent_id": (
                    str(node.parent_id)
                    if node.parent_id
                    else None
                ),
            }
            for node in nodes
        ]


    def _evidence_to_list(
        self,
        evidence: list[EvidenceProfile],
    ) -> list[dict]:

        return [
            {
                "evidence_id": str(item.evidence_id),
                "source_document": (
                    str(item.source_document)
                    if item.source_document
                    else None
                ),
                "evidence_type": item.evidence_type,
                "content": item.content,
                "location": item.location,
                "confidence": item.confidence,
                "metadata": item.metadata,
            }
            for item in evidence
        ]
