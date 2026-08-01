"""
Provenance service tests.
"""

from athena.knowledge.services.provenance_service import (
    ProvenanceService,
)

from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


def test_provenance_extraction():

    obj = KnowledgeObject(
        object_type="document",
        title="Athena",
        confidence=0.95,
        metadata={
            "provider": "docling",
            "source_reference": "demo.pdf",
            "extraction_method": "pdf_extraction",
        },
    )

    service = ProvenanceService()

    result = service.get_provenance(
        obj
    )

    assert (
        result["provider"]
        == "docling"
    )

    assert (
        result["source_reference"]
        == "demo.pdf"
    )

    assert (
        result["extraction_method"]
        == "pdf_extraction"
    )

    assert (
        result["confidence"]
        == 0.95
    )