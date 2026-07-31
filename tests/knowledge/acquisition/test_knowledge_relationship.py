from athena.knowledge.acquisition.domain.knowledge_relationship import (
    KnowledgeRelationship,
)
from uuid import uuid4


def test_relationship_creation():

    source = uuid4()
    target = uuid4()

    relation = KnowledgeRelationship(
        source_object_id=source,
        target_object_id=target,
        relationship_type="supports",
    )

    assert relation.source_object_id == source
    assert relation.target_object_id == target
    assert relation.relationship_type == "supports"


def test_relationship_metadata():

    relation = KnowledgeRelationship()

    relation.add_metadata(
        "origin",
        "semantic_extraction",
    )

    assert relation.metadata["origin"] == "semantic_extraction"