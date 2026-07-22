"""
Unit tests for MetadataService.
"""

from athena.ai.metadata.service import MetadataService


def test_service_finds_document():
    service = MetadataService(
        (
            "My Secret Garden.pdf",
            "Athena Notes.md",
        )
    )

    result = service.detect(
        "Summarize My Secret Garden."
    )

    assert result.found
    assert len(result.documents) == 1
    assert result.documents[0].title == "My Secret Garden.pdf"


def test_service_returns_empty_result():
    service = MetadataService(
        (
            "Python Guide.pdf",
        )
    )

    result = service.detect(
        "Explain quantum computing."
    )

    assert not result.found
    assert result.documents == ()