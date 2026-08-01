from athena.knowledge.acquisition.pipeline.semantic_pass import (
    SemanticPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)


def test_semantic_pass_creates_candidate():

    representation = KnowledgeRepresentation(
        title="Athena Document",
    )

    from uuid import uuid4

    representation.add_node(
        uuid4()
    )

    result = SemanticPass().execute(
        KnowledgeContext(),
        representation,
    )

    assert len(result) == 1

    assert (
        result[0].value
        == "Athena Document"
    )

    assert (
        result[0].confidence
        == 0.5
    )