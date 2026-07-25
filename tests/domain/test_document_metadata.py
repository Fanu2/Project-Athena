
from datetime import datetime
from uuid import uuid4

from athena.domain import DocumentMetadata


def test_document_metadata_defaults():
    metadata = DocumentMetadata(document_id=uuid4())

    assert metadata.language is None
    assert metadata.page_count is None
    assert metadata.last_indexed is None
    assert metadata.metadata_version == 1


def test_document_metadata_values():
    now = datetime.now()
    document_id = uuid4()

    metadata = DocumentMetadata(
        document_id=document_id,
        language="en",
        page_count=12,
        last_indexed=now,
    )

    assert metadata.document_id == document_id
    assert metadata.language == "en"
    assert metadata.page_count == 12
    assert metadata.last_indexed == now
    assert metadata.metadata_version == 1
