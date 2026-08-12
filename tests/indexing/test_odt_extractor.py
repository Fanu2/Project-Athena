"""
Tests for ODT extractor.
"""

from odf.opendocument import OpenDocumentText
from odf.text import P

from athena.indexing.extractors.odt import (
    ODTExtractor,
)


def test_extract_odt(
    tmp_path,
):
    document_path = (
        tmp_path / "sample.odt"
    )

    document = OpenDocumentText()

    document.text.addElement(
        P(
            text="Athena ODT test document",
        )
    )

    document.save(
        str(document_path),
    )

    extractor = ODTExtractor()

    extracted = extractor.extract(
        document_path,
    )

    assert (
        extracted.document_id
        == "sample.odt"
    )

    assert (
        "Athena ODT test document"
        in extracted.text
    )
