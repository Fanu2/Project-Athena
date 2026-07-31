from uuid import uuid4

from athena.knowledge.acquisition.domain.knowledge_node import (
    KnowledgeNode,
)


def test_node_creation():

    node = KnowledgeNode(
        node_type="section",
        content="Introduction",
    )

    assert node.node_type == "section"
    assert node.content == "Introduction"


def test_add_child():

    node = KnowledgeNode()

    child_id = uuid4()

    node.add_child(child_id)

    assert child_id in node.children


def test_node_metadata():

    node = KnowledgeNode()

    node.add_metadata(
        "page",
        5,
    )

    assert node.metadata["page"] == 5