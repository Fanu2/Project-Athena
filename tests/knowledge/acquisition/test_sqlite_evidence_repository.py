"""
SQLite evidence repository tests.
"""

from athena.knowledge.repositories.sqlite_evidence_repository import (
    SQLiteEvidenceRepository,
)

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)


def test_sqlite_evidence_repository(
    tmp_path,
):

    database = (
        tmp_path / "athena.db"
    )

    repository = SQLiteEvidenceRepository(
        str(database)
    )

    evidence = EvidenceRecord(
        source_reference="demo.pdf",
        provider="docling",
    )

    repository.save(
        evidence
    )

    result = (
        repository.list_all()
    )

    assert len(result) == 1

    assert (
        result[0].source_reference
        == "demo.pdf"
    )