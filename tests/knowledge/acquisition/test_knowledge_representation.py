from uuid import uuid4

from athena.knowledge.acquisition.domain.knowledge_representation import (
    KnowledgeRepresentation,
)


def test_representation_creation():

    representation = KnowledgeRepresentation(
        title="Athena Architecture Document",
        representation_type="pdf",
    )

    assert representation.title == "Athena Architecture Document"
    assert representation.representation_type == "pdf"


def test_add_node():

    representation = KnowledgeRepresentation()

    node_id = uuid4()

    representation.add_node(node_id)

    assert node_id in representation.nodes


def test_representation_metadata():

    representation = KnowledgeRepresentation()

    representation.add_metadata(
        "pages",
        20,
    )

    assert representation.metadata["pages"] == 20