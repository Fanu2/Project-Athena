"""
Athena Explainable Knowledge Lifecycle Test

Validates complete AKC flow:

Document
    ->
KnowledgeRepresentation
    ->
KnowledgeObject
    ->
EvidenceRecord
    ->
CitationRecord
"""

from athena.knowledge.acquisition.engine.knowledge_acquisition_engine import (
    KnowledgeAcquisitionEngine,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.providers.docling_provider import (
    DoclingProvider,
)

from athena.knowledge.acquisition.services.provider_manager import (
    ProviderManager,
)

from athena.knowledge.repositories.memory.memory_repository import (
    MemoryKnowledgeRepository,
)

from athena.knowledge.repositories.memory.memory_evidence_repository import (
    MemoryEvidenceRepository,
)

from athena.knowledge.repositories.memory.memory_citation_repository import (
    MemoryCitationRepository,
)

from athena.knowledge.services.evidence_build_service import (
    EvidenceBuildService,
)

from athena.knowledge.services.citation_build_service import (
    CitationBuildService,
)


class FakeArtifact:
    """
    Fake extraction artifact.

    Matches the object contract expected
    by DoclingProvider.
    """

    def __init__(
        self,
        path: str,
    ) -> None:

        self.path = path

        self.title = (
            "Athena Demo"
        )

        self.document_id = (
            path
        )

        self.page_count = 1

        self.text = (
            "Athena knowledge document"
        )


class FakeExtractor:
    """
    Fake document extractor.
    """

    def extract(
        self,
        document,
    ):
        return FakeArtifact(
            document
        )


def test_explainable_knowledge_lifecycle():

    context = KnowledgeContext()

    #
    # Provider setup
    #

    provider_manager = ProviderManager()

    provider_manager.register(
        DoclingProvider(
            extractor=FakeExtractor()
        )
    )

    context.add_service(
        "provider_manager",
        provider_manager,
    )

    #
    # Repository setup
    #

    knowledge_repository = (
        MemoryKnowledgeRepository()
    )

    evidence_repository = (
        MemoryEvidenceRepository()
    )

    citation_repository = (
        MemoryCitationRepository()
    )

    context.add_service(
        "knowledge_repository",
        knowledge_repository,
    )

    #
    # Provenance services
    #

    context.add_service(
        "evidence_build_service",
        EvidenceBuildService(
            evidence_repository
        ),
    )

    context.add_service(
        "citation_build_service",
        CitationBuildService(
            citation_repository
        ),
    )

    #
    # Execute AKC
    #

    engine = KnowledgeAcquisitionEngine()

    result = engine.compile(
        "demo.pdf",
        context,
    )

    #
    # Validate compiler result
    #

    assert result is not None

    assert len(result) == 1

    #
    # Validate KnowledgeObject
    #

    knowledge_objects = (
        knowledge_repository
        .list_all()
    )

    assert len(knowledge_objects) == 1

    knowledge_object = (
        knowledge_objects[0]
    )

    assert (
        knowledge_object.title
        == "Athena Demo"
    )

    #
    # Validate EvidenceRecord
    #

    evidence_records = (
        evidence_repository
        .list_all()
    )

    assert len(evidence_records) == 1

    evidence = (
        evidence_records[0]
    )

    assert (
        evidence.source_reference
        == "demo.pdf"
    )

    #
    # Validate CitationRecord
    #

    citations = (
        citation_repository
        .list_all()
    )

    assert len(citations) == 1

    citation = (
        citations[0]
    )

    assert (
        citation.source_reference
        == "demo.pdf"
    )

    assert (
        citation.evidence_id
        == evidence.evidence_id
    )