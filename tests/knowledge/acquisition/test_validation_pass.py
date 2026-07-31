from athena.knowledge.acquisition.pipeline.validation_pass import (
    ValidationPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)


def test_validation_pass_name():

    stage = ValidationPass()

    assert stage.name == "validation"


def test_validation_pass_execution():

    stage = ValidationPass()

    result = stage.execute(
        KnowledgeContext(),
        "candidate",
    )

    assert result == "candidate"