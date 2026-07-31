from athena.knowledge.acquisition.pipeline.relationship_pass import (
    RelationshipPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_relationship_pass_name():

    stage = RelationshipPass()

    assert stage.name == "relationship"


def test_relationship_pass_execution():

    stage = RelationshipPass()

    result = stage.execute(
        KnowledgeContext(),
        "candidates",
    )

    assert result == "candidates"