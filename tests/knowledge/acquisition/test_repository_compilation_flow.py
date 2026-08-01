"""
Knowledge repository compilation flow tests.
"""

from athena.knowledge.acquisition.engine.knowledge_acquisition_engine import (
    KnowledgeAcquisitionEngine,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.repositories.memory.memory_repository import (
    MemoryKnowledgeRepository,
)

from athena.knowledge.acquisition.providers.docling_provider import (
    DoclingProvider,
)

from athena.knowledge.acquisition.services.provider_manager import (
    ProviderManager,
)


class FakeExtractedDocument:
    """
    Fake extraction result compatible
    with DoclingProvider contract.
    """

    path = "demo.pdf"

    title = "Athena Demo"

    document_id = "demo.pdf"

    page_count = 1

    text = "Knowledge document"


class FakeExtractor:
    """
    Fake document extractor.
    """

    def extract(
        self,
        document,
    ):
        return FakeExtractedDocument()


def test_compilation_persists_knowledge():

    context = KnowledgeContext()

    #
    # Repository
    #

    repository = (
        MemoryKnowledgeRepository()
    )

    context.add_service(
        "knowledge_repository",
        repository,
    )

    #
    # Provider
    #

    manager = ProviderManager()

    manager.register(
        DoclingProvider(
            extractor=FakeExtractor()
        )
    )

    context.add_service(
        "provider_manager",
        manager,
    )

    #
    # Compile
    #

    engine = KnowledgeAcquisitionEngine()

    result = engine.compile(
        "demo.pdf",
        context,
    )

    #
    # Assertions
    #

    assert result is not None

    stored = (
        repository.list_all()
    )

    assert len(stored) == 1

    assert (
        stored[0].title
        == "Athena Demo"
    )

    assert (
        stored[0].metadata["provider"]
        == "docling"
    )