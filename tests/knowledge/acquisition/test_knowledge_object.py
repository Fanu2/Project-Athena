from athena.knowledge.acquisition.domain.knowledge_object import (
    KnowledgeObject,
)


def test_knowledge_object_creation():

    obj = KnowledgeObject(
        object_type="document",
        title="Athena Test",
    )

    assert obj.title == "Athena Test"
    assert obj.object_type == "document"
    assert obj.object_id is not None


def test_metadata_update():

    obj = KnowledgeObject()

    obj.update_metadata(
        "source",
        "test.pdf",
    )

    assert obj.metadata["source"] == "test.pdf"