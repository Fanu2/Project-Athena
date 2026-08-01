from athena.knowledge.acquisition.pipeline.validation_pass import (
    ValidationPass,
)

from athena.knowledge.acquisition.domain.knowledge_candidate import (
    KnowledgeCandidate,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_validation_accepts_candidate():

    candidate = KnowledgeCandidate(
        value="Athena"
    )

    result = ValidationPass().execute(
        KnowledgeContext(),
        [candidate],
    )

    assert len(result) == 1