from dataclasses import dataclass

from athena.evaluation.score_explanation_engine import ScoreExplanationEngine


@dataclass
class Candidate:
    semantic_score: float
    keyword_score: float
    metadata_score: float
    identity_score: float


def test_score_explanation_engine():

    candidate = Candidate(
        semantic_score=0.91,
        keyword_score=0.82,
        metadata_score=0.55,
        identity_score=1.00,
    )

    engine = ScoreExplanationEngine()

    explanations = engine.explain(candidate)

    assert len(explanations) == 4
    assert "semantic" in explanations[0].lower()
    assert "identity" in explanations[-1].lower()

