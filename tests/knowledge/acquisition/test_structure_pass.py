from athena.knowledge.acquisition.pipeline.structure_pass import (
    StructurePass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)


def test_structure_pass_name():

    stage = StructurePass()

    assert stage.name == "structure"


def test_structure_pass_creates_representation():

    stage = StructurePass()

    result = stage.execute(
        KnowledgeContext(),
        "test document",
    )

    assert isinstance(
        result,
        KnowledgeRepresentation,
    )

    assert result.title == "test document"