from athena.retrieval.query_filters import (
    FILE_TYPES,
    LANGUAGES,
    OPERATIONS,
)


def test_language_set():
    assert "hindi" in LANGUAGES
    assert "urdu" in LANGUAGES
    assert "persian" in LANGUAGES


def test_file_types():
    assert "pdf" in FILE_TYPES
    assert "epub" in FILE_TYPES


def test_operations():
    assert "summarize" in OPERATIONS
    assert "compare" in OPERATIONS
