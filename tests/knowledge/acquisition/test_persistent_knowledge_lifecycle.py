"""
Athena Persistent Knowledge Lifecycle Test

Validates:

Document
    ->
KnowledgeObject
    ->
EvidenceRecord
    ->
CitationRecord
    ->
Database Restart
    ->
Retrieval
"""

from athena.knowledge.repositories.sqlite_evidence_repository import (
    SQLiteEvidenceRepository,
)

from athena.knowledge.repositories.sqlite_citation_repository import (
    SQLiteCitationRepository,
)

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)

from athena.knowledge.acquisition.domain.citation_record import (
    CitationRecord,
)


def test_persistent_provenance_survives_restart(
    tmp_path,
):

    database = (
        tmp_path / "athena.db"
    )

    #
    # Runtime 1
    #

    evidence_repository = (
        SQLiteEvidenceRepository(
            str(database)
        )
    )

    citation_repository = (
        SQLiteCitationRepository(
            str(database)
        )
    )

    evidence = EvidenceRecord(
        source_reference="demo.pdf",
        provider="docling",
        extraction_method="docling",
    )

    evidence_repository.save(
        evidence
    )

    citation = CitationRecord(
        evidence_id=(
            evidence.evidence_id
        ),
        source_reference="demo.pdf",
        citation_text="Athena Demo",
    )

    citation_repository.save(
        citation
    )

    #
    # Runtime 2
    # Simulate restart
    #

    evidence_repository_2 = (
        SQLiteEvidenceRepository(
            str(database)
        )
    )

    citation_repository_2 = (
        SQLiteCitationRepository(
            str(database)
        )
    )

    stored_evidence = (
        evidence_repository_2
        .list_all()
    )

    stored_citations = (
        citation_repository_2
        .list_all()
    )

    assert len(
        stored_evidence
    ) == 1

    assert len(
        stored_citations
    ) == 1

    assert (
        stored_evidence[0]
        .source_reference
        == "demo.pdf"
    )

    assert (
        stored_citations[0]
        .source_reference
        == "demo.pdf"
    )