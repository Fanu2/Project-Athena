from athena.knowledge.acquisition.domain.evidence_record import (
    EvidenceRecord,
)


def test_evidence_creation():

    evidence = EvidenceRecord(
        source_reference="paper.pdf",
        location="page 10",
        provider="docling",
    )

    assert evidence.source_reference == "paper.pdf"
    assert evidence.location == "page 10"
    assert evidence.provider == "docling"


def test_evidence_metadata():

    evidence = EvidenceRecord()

    evidence.add_metadata(
        "format",
        "pdf",
    )

    assert evidence.metadata["format"] == "pdf"