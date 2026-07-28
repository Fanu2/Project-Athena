from pathlib import Path

from athena.ai.citations import CitationFormatter
from athena.ai.rag.models import RAGSource


def test_formatter():

    source = RAGSource(
        chunk_id="chunk1",
        document_id="doc1",
        document_name="Manual.pdf",
        document_path=Path("Manual.pdf"),
        page_number=12,
        score=0.91,
        text="Example text",
    )

    text = CitationFormatter.format(source)

    assert "Manual.pdf" in text
    assert "Page 12" in text
    assert "0.91" in text
