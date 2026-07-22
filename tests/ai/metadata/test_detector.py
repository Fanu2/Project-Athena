"""
Unit tests for MetadataDetector.
"""

from athena.ai.metadata.detector import MetadataDetector


def test_detector_finds_document():
    detector = MetadataDetector(
        (
            "My Secret Garden.pdf",
            "Athena Notes.md",
        )
    )

    result = detector.detect(
        "Summarize My Secret Garden."
    )

    assert result.found
    assert len(result.documents) == 1
    assert result.documents[0].title == "My Secret Garden.pdf"


def test_detector_returns_empty_result():
    detector = MetadataDetector(
        (
            "Python Guide.pdf",
        )
    )

    result = detector.detect(
        "Explain quantum computing."
    )

    assert not result.found
    assert result.documents == ()