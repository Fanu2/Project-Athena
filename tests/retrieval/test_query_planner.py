from athena.retrieval.query_planner import QueryPlanner


def test_detect_language():
    planner = QueryPlanner()

    intent = planner.parse("Summarize the Hindi documents")

    assert intent.semantic_query == "summarize"
    assert intent.languages == ("Hindi",)


def test_detect_file_type():
    planner = QueryPlanner()

    intent = planner.parse("Search pdf only")

    assert intent.semantic_query == "search"
    assert intent.file_types == ("pdf",)


def test_detect_multiple_languages():
    planner = QueryPlanner()

    intent = planner.parse("Compare Urdu and Persian documents")

    assert set(intent.languages) == {"Urdu", "Persian"}


def test_detect_language_and_file_type():
    planner = QueryPlanner()

    intent = planner.parse("Summarize Hindi PDF documents")

    assert intent.semantic_query == "summarize"
    assert intent.languages == ("Hindi",)
    assert intent.file_types == ("pdf",)

