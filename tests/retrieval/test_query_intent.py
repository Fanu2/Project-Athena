from athena.retrieval.query_intent import QueryIntent


def test_query_intent_defaults():
    intent = QueryIntent(
        original_query="Search PDFs",
        semantic_query="search",
    )

    assert intent.original_query == "Search PDFs"
    assert intent.semantic_query == "search"

    assert intent.languages == ()
    assert intent.file_types == ()
    assert intent.document_names == ()
    assert intent.collections == ()

    assert dict(intent.filters) == {}

