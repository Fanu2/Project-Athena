"""
Tests for Athena citation persistence.
"""

from __future__ import annotations

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)

from athena.knowledge.repositories.sqlite_citation_repository import (
    SQLiteCitationRepository,
)

from athena.knowledge.services.citation_build_service import (
    CitationBuildService,
)


def test_citation_build_service_persists_record(
    tmp_path,
) -> None:
    """
    Citation records are persisted in SQLite.
    """

    database = (
        tmp_path / "citation.db"
    )

    repository = SQLiteCitationRepository(
        str(database),
    )

    service = CitationBuildService(
        repository,
    )

    evidence = EvidenceRecord(
        source_reference="/tmp/athena.pdf",
        location="/page/1",
        extraction_method="pdf",
        provider="docling",
        confidence=1.0,
    )

    citation = service.build(
        evidence,
    )

    records = repository.list_all()

    assert len(records) == 1

    stored = records[0]

    assert (
        stored.citation_id
        == citation.citation_id
    )

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