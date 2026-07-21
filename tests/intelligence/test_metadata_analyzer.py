from athena.indexing.models import (
    ExtractedDocument,
    ExtractedPage,
)

from athena.intelligence.analyzers.metadata_analyzer import (
    MetadataAnalyzer,
)


def test_metadata_analyzer():
    document = ExtractedDocument(
        document_id="doc-1",
        path=None,
        title="Test",
        text="Hello world\nThis is Athena.",
        pages=(
            ExtractedPage(
                page_number=1,
                text="Hello world\nThis is Athena.",
            ),
        ),
        page_count=1,
    )

    metadata = MetadataAnalyzer().analyze(document)

    assert metadata.word_count == 5
    assert metadata.character_count == len(document.text)
    assert metadata.line_count == 2
    assert metadata.page_count == 1
    assert metadata.estimated_reading_minutes == 1
