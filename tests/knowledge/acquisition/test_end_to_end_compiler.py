"""
AKC End-to-End Compiler Acceptance Test
"""

from pathlib import Path

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

from athena.indexing.models import (
    ExtractedDocument,
    ExtractedPage,
)


class FakeExtractor:
    """
    Fake document extractor for compiler test.
    """

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:

        return ExtractedDocument(
            document_id="demo.pdf",
            path=document,
            title="Athena Demo",
            text="Athena knowledge",
            pages=(
                ExtractedPage(
                    page_number=1,
                    text="Athena knowledge",
                ),
            ),
            page_count=1,
        )


class FakeIndexer:
    """
    Fake indexer to verify IndexPass integration.
    """

    def __init__(self):
        self.indexed = []

    def index(
        self,
        knowledge,
    ) -> None:

        self.indexed.append(
            knowledge
        )


def test_end_to_end_compiler():

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
    # Indexer setup
    #

    indexer = FakeIndexer()

    context.add_service(
        "knowledge_indexer",
        indexer,
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
    # Assertions
    #

    assert result is not None

    assert len(result) == 1

    knowledge = result[0]

    assert knowledge.title == "Athena Demo"

    assert (
        knowledge.object_type
        == "document"
    )

    assert (
        len(indexer.indexed)
        == 1
    )