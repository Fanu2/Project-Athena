from athena.ai.citations import CitationAdapter
from athena.ai.retrieval.models import SemanticResult


def test_from_semantic_result():

    result = SemanticResult(
        chunk_id="chunk1",
        document_id="doc1",
        document_title="Guide.pdf",
        page_number=2,
        start_offset=10,
        end_offset=80,
        text="Athena",
        score=0.95,
    )

    citation = CitationAdapter.from_semantic_result(result)

    assert citation.document_id == "doc1"
    assert citation.title == "Guide.pdf"
    assert citation.page_number == 2
    assert citation.start_offset == 10
    assert citation.end_offset == 80
    assert citation.score == 0.95
