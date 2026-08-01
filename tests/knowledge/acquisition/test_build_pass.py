from athena.knowledge.acquisition.pipeline.build_pass import (
    BuildPass,
)

from athena.knowledge.acquisition.domain.knowledge_candidate import (
    KnowledgeCandidate,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_build_pass_creates_knowledge_object():

    candidate = KnowledgeCandidate(
        candidate_type="document",
        value="Athena",
        confidence=0.8,
    )

    result = BuildPass().execute(
        KnowledgeContext(),
        [candidate],
    )

    assert len(result) == 1

    obj = result[0]

    assert obj.object_type == "document"

    assert obj.title == "Athena"

    assert obj.confidence == 0.8