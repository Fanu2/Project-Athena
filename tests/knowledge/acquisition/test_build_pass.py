from athena.knowledge.acquisition.pipeline.build_pass import (
    BuildPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_build_pass_name():

    stage = BuildPass()

    assert stage.name == "build"


def test_build_pass_execution():

    stage = BuildPass()

    result = stage.execute(
        KnowledgeContext(),
        "validated knowledge",
    )

    assert result == "validated knowledge"