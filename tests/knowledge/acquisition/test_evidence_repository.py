"""
Evidence repository tests.
"""

from athena.knowledge.repositories.memory.memory_evidence_repository import (
    MemoryEvidenceRepository,
)

from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)


def test_memory_evidence_repository():

    repository = (
        MemoryEvidenceRepository()
    )

    evidence = EvidenceRecord()

    repository.save(
        evidence
    )

    result = (
        repository.list_all()
    )

    assert len(result) == 1