"""
Evidence build service tests.
"""

from athena.knowledge.services.evidence_build_service import (
    EvidenceBuildService,
)

from athena.knowledge.repositories.memory.memory_evidence_repository import (
    MemoryEvidenceRepository,
)

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


def test_evidence_build_service():

    repository = (
        MemoryEvidenceRepository()
    )

    service = EvidenceBuildService(
        repository
    )

    knowledge = KnowledgeObject(
        title="Athena Demo",
        metadata={
            "source_path": "demo.pdf",
            "provider": "docling",
            "extraction_method": "docling",
        },
    )

    evidence = service.build(
        knowledge
    )

    assert evidence is not None

    stored = (
        repository.list_all()
    )

    assert len(stored) == 1

    assert (
        stored[0].source_reference
        == "demo.pdf"
    )