from athena.ai.retrieval.identity_ranker import IdentityRanker


def test_exact_document_match() -> None:
    ranker = IdentityRanker()

    assert (
        ranker.score(
            "constitution.md",
            "01-CONSTITUTION.md",
        )
        == 1.0
    )


def test_partial_document_match() -> None:
    ranker = IdentityRanker()

    assert (
        ranker.score(
            "SAS-v1.0",
            "SAS-v1.0-Draft.md",
        )
        == 0.5
    )


def test_unrelated_document() -> None:
    ranker = IdentityRanker()

    assert (
        ranker.score(
            "constitution",
            "04-GLOSSARY.md",
        )
        == 0.0
    )


def test_implementation_query_prefers_service_file() -> None:
    ranker = IdentityRanker()

    service_score = ranker.score(
        "Where is semantic retrieval implemented?",
        "service.py",
    )

    context_score = ranker.score(
        "Where is semantic retrieval implemented?",
        "application_context.py",
    )

    assert service_score > context_score
    assert service_score > 0.0


def test_implementation_query_prefers_repository_file() -> None:
    ranker = IdentityRanker()

    repository_score = ranker.score(
        "Where is document storage implemented?",
        "repository.py",
    )

    service_score = ranker.score(
        "Where is document storage implemented?",
        "service.py",
    )

    assert repository_score > service_score
