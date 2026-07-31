from athena.knowledge.acquisition.pipeline.semantic_pass import (
    SemanticPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_semantic_pass_name():

    stage = SemanticPass()

    assert stage.name == "semantic"


def test_semantic_pass_execution():

    stage = SemanticPass()

    result = stage.execute(
        KnowledgeContext(),
        "representation",
    )

    assert result == "representation"