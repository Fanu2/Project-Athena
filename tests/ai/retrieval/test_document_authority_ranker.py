from athena.ai.retrieval.document_authority_ranker import (
    DocumentAuthorityRanker,
)


def test_specification_has_high_authority():

    ranker = DocumentAuthorityRanker()

    score = ranker.score(
        "RIE-Specification-v1.0.md"
    )

    assert score == 0.20


def test_source_code_has_no_authority():

    ranker = DocumentAuthorityRanker()

    score = ranker.score(
        "service.py",
        "documents/code/service.py",
    )

    assert score == 0.0


def test_guide_has_authority():

    ranker = DocumentAuthorityRanker()

    score = ranker.score(
        "Testing-Benchmark-Guide-v1.0.md"
    )

    assert score == 0.15
