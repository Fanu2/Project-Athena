from pathlib import Path

from athena.documents.storage import DocumentStorage


def test_copy_document(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("Hello Athena")

    documents_dir = tmp_path / "documents"

    copied = DocumentStorage.copy_document(source, documents_dir)

    assert copied.exists()
    assert copied.read_text() == "Hello Athena"


def test_remove_document(tmp_path):
    file = tmp_path / "delete.txt"
    file.write_text("temporary")

    DocumentStorage.remove_document(file)

    assert not file.exists()


def test_list_documents_empty(tmp_path):
    documents_dir = tmp_path / "documents"

    docs = DocumentStorage.list_documents(documents_dir)

    assert docs == []


def test_list_documents_single(tmp_path):
    documents_dir = tmp_path / "documents"
    documents_dir.mkdir()

    (documents_dir / "sample.txt").write_text("hello")

    docs = DocumentStorage.list_documents(documents_dir)

    assert len(docs) == 1
    assert docs[0].name == "sample.txt"


def test_list_documents_multiple(tmp_path):
    documents_dir = tmp_path / "documents"
    documents_dir.mkdir()

    (documents_dir / "a.txt").write_text("A")
    (documents_dir / "b.md").write_text("B")
    (documents_dir / "c.pdf").write_text("C")

    docs = DocumentStorage.list_documents(documents_dir)

    assert len(docs) == 3

    names = [doc.name for doc in docs]

    assert "a.txt" in names
    assert "b.md" in names
    assert "c.pdf" in names