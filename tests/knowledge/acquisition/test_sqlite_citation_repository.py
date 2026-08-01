"""
SQLite citation repository tests.
"""

from athena.knowledge.repositories.sqlite_citation_repository import (
    SQLiteCitationRepository,
)

from athena.knowledge.acquisition.domain.citation_record import (
    CitationRecord,
)


def test_sqlite_citation_repository(
    tmp_path,
):

    database = (
        tmp_path / "athena.db"
    )

    repository = SQLiteCitationRepository(
        str(database)
    )

    citation = CitationRecord(
        source_reference="demo.pdf",
        citation_text="Athena Demo",
    )

    repository.save(
        citation
    )

    result = (
        repository.list_all()
    )

    assert len(result) == 1

    assert (
        result[0].source_reference
        == "demo.pdf"
    )