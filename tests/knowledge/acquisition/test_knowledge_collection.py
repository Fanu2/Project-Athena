from uuid import uuid4

from athena.knowledge.acquisition.domain.knowledge_collection import (
    KnowledgeCollection,
)


def test_collection_creation():

    collection = KnowledgeCollection(
        name="Athena Research",
        collection_type="project",
    )

    assert collection.name == "Athena Research"
    assert collection.collection_type == "project"


def test_add_object():

    collection = KnowledgeCollection()

    object_id = uuid4()

    collection.add_object(object_id)

    assert object_id in collection.object_ids


def test_collection_metadata():

    collection = KnowledgeCollection()

    collection.add_metadata(
        "owner",
        "athena",
    )

    assert collection.metadata["owner"] == "athena"