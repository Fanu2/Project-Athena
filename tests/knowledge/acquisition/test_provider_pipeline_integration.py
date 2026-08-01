"""
Provider pipeline integration tests.

Validates that ImportPass uses the registered
acquisition provider and produces a
KnowledgeRepresentation.
"""

from pathlib import Path

from athena.indexing.models import (
    ExtractedDocument,
    ExtractedPage,
)

from athena.knowledge.acquisition.providers.docling_provider import (
    DoclingProvider,
)

from athena.knowledge.acquisition.services.provider_manager import (
    ProviderManager,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.pipeline.import_pass import (
    ImportPass,
)


class FakeExtractor:
    """
    Fake extractor for provider isolation.
    """

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:

        return ExtractedDocument(
            document_id="test.pdf",
            path=document,
            title="Test Document",
            text="Athena test content",
            pages=(
                ExtractedPage(
                    page_number=1,
                    text="Athena test content",
                ),
            ),
            page_count=1,
        )


def test_import_pass_uses_provider():

    manager = ProviderManager()

    manager.register(
        DoclingProvider(
            extractor=FakeExtractor()
        )
    )

    context = KnowledgeContext()

    context.add_service(
        "provider_manager",
        manager,
    )

    result = ImportPass().execute(
        context,
        "test.pdf",
    )

    assert result is not None

    assert (
        result.title
        == "Test Document"
    )

    assert (
        result.metadata["provider"]
        == "docling"
    )