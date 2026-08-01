from pathlib import Path

from athena.indexing.models import (
    ExtractedDocument,
    ExtractedPage,
)

from athena.knowledge.acquisition.providers.docling_provider import (
    DoclingProvider,
)


class FakeExtractor:

    def extract(
        self,
        document: Path,
    ):

        return ExtractedDocument(
            document_id="test.pdf",
            path=document,
            title="Test Document",
            text="Athena knowledge",
            pages=(
                ExtractedPage(
                    page_number=1,
                    text="Athena knowledge",
                ),
            ),
            page_count=1,
        )


def test_docling_provider_name():

    provider = DoclingProvider(
        extractor=FakeExtractor()
    )

    assert provider.name == "docling"


def test_docling_provider_capability():

    provider = DoclingProvider(
        extractor=FakeExtractor()
    )

    assert (
        "document_structure_extraction"
        in provider.capabilities
    )


def test_docling_returns_import_artifact():

    provider = DoclingProvider(
        extractor=FakeExtractor()
    )

    artifact = provider.execute(
        "document_structure_extraction",
        "test.pdf",
    )

    assert artifact.artifact_type == "document"
    assert artifact.metadata["title"] == "Test Document"
    assert artifact.metadata["page_count"] == 1