"""
Unit tests for MetadataMatcher.
"""

from athena.ai.metadata.matcher import MetadataMatcher


def test_exact_match():
    matcher = MetadataMatcher(
        (
            "My Secret Garden.pdf",
            "Athena Notes.md",
        )
    )

    result = matcher.match(
        "Summarize My Secret Garden."
    )

    assert len(result) == 1
    assert result[0].title == "My Secret Garden.pdf"


def test_case_insensitive_match():
    matcher = MetadataMatcher(
        (
            "My Secret Garden.pdf",
        )
    )

    result = matcher.match(
        "summarize my secret garden"
    )

    assert len(result) == 1


def test_no_match():
    matcher = MetadataMatcher(
        (
            "Python Guide.pdf",
        )
    )

    result = matcher.match(
        "Explain quantum computing."
    )

    assert result == ()


def test_multiple_matches():
    matcher = MetadataMatcher(
        (
            "Einstein.pdf",
            "Newton.pdf",
        )
    )

    result = matcher.match(
        "Compare Einstein and Newton."
    )

    assert len(result) == 2


def test_filename_extension_ignored():
    matcher = MetadataMatcher(
        (
            "Athena Design Notes.md",
        )
    )

    result = matcher.match(
        "Summarize Athena Design Notes."
    )

    assert len(result) == 1