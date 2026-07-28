from athena.ai.retrieval.evidence_explainer import (
    EvidenceExplainer,
)


def test_explainer_generates_reasons() -> None:
    """Strong signals should create explanations."""

    explainer = EvidenceExplainer()

    reasons = explainer.explain(
        semantic_score=0.9,
        keyword_score=0.8,
        metadata_score=0.0,
        identity_score=0.6,
        document_authority_score=0.7,
    )

    assert "Strong semantic similarity" in reasons
    assert "Keyword match found" in reasons
    assert "High document authority" in reasons


def test_explainer_has_fallback() -> None:
    """Weak signals should still explain retrieval."""

    explainer = EvidenceExplainer()

    reasons = explainer.explain(
        semantic_score=0.1,
        keyword_score=0.0,
        metadata_score=0.0,
        identity_score=0.0,
        document_authority_score=0.0,
    )

    assert (
        "Relevant semantic evidence retrieved"
        in reasons
    )
