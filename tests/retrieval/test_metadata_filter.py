from dataclasses import dataclass

from athena.retrieval.metadata_filter import MetadataFilter
from athena.retrieval.query_intent import QueryIntent


@dataclass
class MockDocument:
    """Simple document used for MetadataFilter unit tests."""

    language: str
    file_type: str


def test_filter_by_language():
    documents = [
        MockDocument("Hindi", "pdf"),
        MockDocument("Urdu", "pdf"),
    ]

    intent = QueryIntent(
        original_query="",
        semantic_query="search",
        languages=("Hindi",),
    )

    filtered = MetadataFilter().filter(documents, intent)

    assert len(filtered) == 1
    assert filtered[0].language == "Hindi"


def test_filter_by_file_type():
    documents = [
        MockDocument("Hindi", "pdf"),
        MockDocument("Hindi", "epub"),
    ]

    intent = QueryIntent(
        original_query="",
        semantic_query="search",
        file_types=("pdf",),
    )

    filtered = MetadataFilter().filter(documents, intent)

    assert len(filtered) == 1
    assert filtered[0].file_type == "pdf"


def test_filter_by_language_and_file_type():
    documents = [
        MockDocument("Hindi", "pdf"),
        MockDocument("Hindi", "epub"),
        MockDocument("Urdu", "pdf"),
    ]

    intent = QueryIntent(
        original_query="",
        semantic_query="search",
        languages=("Hindi",),
        file_types=("pdf",),
    )

    filtered = MetadataFilter().filter(documents, intent)

    assert len(filtered) == 1
    assert filtered[0].language == "Hindi"
    assert filtered[0].file_type == "pdf"


def test_no_filters_returns_all():
    documents = [
        MockDocument("Hindi", "pdf"),
        MockDocument("Urdu", "epub"),
    ]

    intent = QueryIntent(
        original_query="",
        semantic_query="search",
    )

    filtered = MetadataFilter().filter(documents, intent)

    assert len(filtered) == 2
    assert filtered == documents

