"""
Citation build service tests.
"""

from athena.knowledge.services.citation_build_service import (
    CitationBuildService,
)

from athena.knowledge.repositories.memory.memory_citation_repository import (
    MemoryCitationRepository,
)

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)


def test_citation_build_service():

    repository = (
        MemoryCitationRepository()
    )

    service = CitationBuildService(
        repository
    )

    evidence = EvidenceRecord(
        source_reference="demo.pdf",
        provider="docling",
        extraction_method="docling",
        confidence=0.9,
    )

    citation = service.build(
        evidence
    )

    assert citation is not None

    stored = (
        repository.list_all()
    )

    assert len(stored) == 1

    assert (
        stored[0].source_reference
        == "demo.pdf"
    )

    assert (
        stored[0].metadata["provider"]
        == "docling"
    )