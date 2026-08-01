from pathlib import Path

from athena.knowledge.acquisition.pipeline.import_pass import (
    ImportPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.services.provider_manager import (
    ProviderManager,
)

from athena.knowledge.acquisition.providers.docling_provider import (
    DoclingProvider,
)

from athena.indexing.models import (
    ExtractedDocument,
    ExtractedPage,
)


class FakeExtractor:

    def extract(
        self,
        document: Path,
    ):

        return ExtractedDocument(
            document_id="demo.pdf",
            path=document,
            title="Demo",
            text="Athena",
            pages=(
                ExtractedPage(
                    page_number=1,
                    text="Athena",
                ),
            ),
            page_count=1,
        )


def test_import_creates_knowledge_representation():

    provider = DoclingProvider(
        extractor=FakeExtractor()
    )

    manager = ProviderManager()

    manager.register(provider)

    context = KnowledgeContext()

    context.add_service(
        "provider_manager",
        manager,
    )

    result = ImportPass().execute(
        context,
        "demo.pdf",
    )

    assert (
        result.representation_type
        == "document"
    )

    assert result.title == "Demo"