"""
Tests for SQLite document intelligence repository.
"""

from __future__ import annotations

from athena.knowledge.intelligence.document_intelligence import (
    DocumentIntelligence,
)

from athena.knowledge.intelligence.document_profile import (
    DocumentProfile,
)

from athena.knowledge.intelligence.document_metadata_profile import (
    DocumentMetadataProfile,
)

from athena.knowledge.intelligence.document_structure import (
    DocumentStructureNode,
)

from athena.knowledge.intelligence.evidence_profile import (
    EvidenceProfile,
)

from athena.knowledge.repositories.sqlite_document_intelligence_repository import (
    SQLiteDocumentIntelligenceRepository,
)


def test_document_intelligence_save_and_get(
    tmp_path,
) -> None:
    """
    Verify document intelligence persistence.
    """

    database = (
        tmp_path / "intelligence.db"
    )

    repository = (
        SQLiteDocumentIntelligenceRepository(
            str(database),
        )
    )


    intelligence = DocumentIntelligence(
        profile=DocumentProfile(
            title="Athena Guide",
            document_type="pdf",
            page_count=10,
            section_count=3,
            entity_count=5,
        ),
        metadata=DocumentMetadataProfile(
            document_type="pdf",
            language="en",
            author="Athena",
        ),
        structure=[
            DocumentStructureNode(
                node_type="section",
                title="Introduction",
                level=1,
            )
        ],
        evidence=[
            EvidenceProfile(
                evidence_type="text",
                content="Athena is offline AI.",
                location="page 1",
            )
        ],
    )


    repository.save(
        "document-001",
        intelligence,
    )


    loaded = repository.get(
        "document-001",
    )


    assert loaded is not None

    assert (
        loaded.profile.title
        == "Athena Guide"
    )

    assert (
        loaded.metadata.language
        == "en"
    )

    assert len(
        loaded.structure
    ) == 1

    assert len(
        loaded.evidence
    ) == 1

    assert (
        loaded.evidence[0].content
        == "Athena is offline AI."
    )
