"""
Tests for citation formatter.
"""

from __future__ import annotations

from athena.ai.citations import Citation
from athena.ai.citations import CitationFormatter


def test_format_citation() -> None:
    """Citation formatter produces readable output."""

    citation = Citation(
        document_id="doc-1",
        title="AI Safety.pdf",
        page_number=18,
        start_offset=1540,
        end_offset=2012,
        score=0.943,
    )

    formatted = CitationFormatter.format(
        citation,
    )

    assert "AI Safety.pdf" in formatted
    assert "Page 18" in formatted
    assert "1540" in formatted
    assert "2012" in formatted
    assert "Similarity 0.94" in formatted
