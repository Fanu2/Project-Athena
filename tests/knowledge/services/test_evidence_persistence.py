"""
Tests for Athena evidence persistence.
"""

from __future__ import annotations

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)

from athena.knowledge.repositories.sqlite_evidence_repository import (
    SQLiteEvidenceRepository,
)

from athena.knowledge.services.evidence_build_service import (
    EvidenceBuildService,
)


def test_evidence_build_service_persists_record(
    tmp_path,
) -> None:
    """
    Evidence records are persisted in SQLite.
    """

    database = (
        tmp_path / "evidence.db"
    )

    repository = SQLiteEvidenceRepository(
        str(database),
    )

    service = EvidenceBuildService(
        repository,
    )

    knowledge = KnowledgeObject(
        object_type="document",
        title="Athena",
        metadata={
            "source_path": "/tmp/athena.pdf",
            "provider": "docling",
            "extraction_method": "pdf",
        },
    )

    evidence = service.build(
        knowledge,
    )

    records = repository.list_all()

    assert len(records) == 1

    stored = records[0]

    assert (
        stored.evidence_id
        == evidence.evidence_id
    )

    assert (
        stored.source_reference
        == "/tmp/athena.pdf"
    )

    assert (
        stored.confidence
        == 1.0
    )