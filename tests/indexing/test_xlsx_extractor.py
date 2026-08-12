"""
Tests for XLSX extractor.
"""

from openpyxl import Workbook

from athena.indexing.extractors.xlsx import (
    XLSXExtractor,
)


def test_extract_xlsx(
    tmp_path,
):
    document_path = (
        tmp_path / "owners.xlsx"
    )

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "Owners"

    sheet.append(
        [
            "Name",
            "Khewat",
            "Share",
        ]
    )

    sheet.append(
        [
            "Ram Singh",
            "124",
            "1/2",
        ]
    )

    workbook.save(
        document_path,
    )

    extracted = XLSXExtractor().extract(
        document_path,
    )

    assert (
        extracted.document_id
        == "owners.xlsx"
    )

    assert "Owners" in extracted.text
    assert "Ram Singh" in extracted.text
    assert "124" in extracted.text
