from pathlib import Path

import pytest

from athena.documents.exceptions import InvalidDocumentError
from athena.documents.validators import validate_document


def test_missing_document():
    with pytest.raises(InvalidDocumentError):
        validate_document(Path("missing.pdf"))


def test_directory_not_document(tmp_path):
    with pytest.raises(InvalidDocumentError):
        validate_document(tmp_path)


def test_invalid_extension(tmp_path):
    file = tmp_path / "notes.docx"
    file.write_text("hello")

    with pytest.raises(InvalidDocumentError):
        validate_document(file)


def test_valid_pdf(tmp_path):
    file = tmp_path / "sample.pdf"
    file.write_text("dummy")

    assert validate_document(file) == file


def test_valid_txt(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("dummy")

    assert validate_document(file) == file


def test_valid_md(tmp_path):
    file = tmp_path / "sample.md"
    file.write_text("dummy")

    assert validate_document(file) == file
