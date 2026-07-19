from datetime import datetime
from pathlib import Path

from athena.indexing.models import IndexedDocument
from athena.indexing.repositories.sqlite_document import (
    SQLiteDocumentRepository,
)
from athena.indexing.services.document_library import (
    DocumentLibraryService,
)


def test_list_documents(tmp_path):
    repository = SQLiteDocumentRepository(
        tmp_path / "athena.db",
    )

    repository.save_document(
        IndexedDocument(
            document_id="1",
            path=Path("alpha.pdf"),
            title="Alpha",
            sha256="111",
            page_count=5,
            indexed_at=datetime.now(),
        )
    )

    service = DocumentLibraryService(
        repository,
    )

    documents = service.list_documents()

    assert len(documents) == 1
    assert documents[0].title == "Alpha"


def test_search_by_title(tmp_path):
    repository = SQLiteDocumentRepository(
        tmp_path / "athena.db",
    )

    repository.save_document(
        IndexedDocument(
            document_id="1",
            path=Path("guide.pdf"),
            title="Python Guide",
            sha256="111",
            page_count=12,
            indexed_at=datetime.now(),
        )
    )

    service = DocumentLibraryService(
        repository,
    )

    results = service.search_by_title(
        "Python",
    )

    assert len(results) == 1
    assert results[0].title == "Python Guide"
