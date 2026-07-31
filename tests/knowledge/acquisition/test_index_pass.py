from athena.knowledge.acquisition.pipeline.index_pass import (
    IndexPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_index_pass_name():

    stage = IndexPass()

    assert stage.name == "index"


def test_index_pass_execution():

    stage = IndexPass()

    result = stage.execute(
        KnowledgeContext(),
        "knowledge object",
    )

    assert result == "knowledge object"