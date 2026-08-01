from athena.knowledge.acquisition.pipeline.structure_pass import (
    StructurePass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)


def test_structure_pass_creates_document_node():

    representation = KnowledgeRepresentation(
        title="Athena Document",
    )

    result = StructurePass().execute(
        KnowledgeContext(),
        representation,
    )

    assert len(result.nodes) == 1