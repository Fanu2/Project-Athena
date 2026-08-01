"""
Citation repository tests.
"""

from athena.knowledge.repositories.memory.memory_citation_repository import (
    MemoryCitationRepository,
)

from athena.knowledge.acquisition.domain.citation_record import (
    CitationRecord,
)


def test_memory_citation_repository():

    repository = (
        MemoryCitationRepository()
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