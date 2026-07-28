from pathlib import Path

from athena.indexing.extractors.epub import EPUBExtractor


def test_epub_extraction() -> None:
    """Verify that text can be extracted from an EPUB document."""

    extractor = EPUBExtractor()

    epub_files = sorted(Path("tests/data/epub").glob("*.epub"))

    assert epub_files, "No EPUB files found."

    # Use the first EPUB that isn't the known-bad letters.epub
    document = next(epub for epub in epub_files if epub.name != "letters.epub")

    result = extractor.extract(document)

    assert result.text.strip()
    assert result.title
    assert result.page_count > 0

