from uuid import uuid4

from athena.knowledge.acquisition.domain.knowledge_candidate import (
    KnowledgeCandidate,
)


def test_candidate_creation():

    node_id = uuid4()

    candidate = KnowledgeCandidate(
        candidate_type="person",
        value="Albert Einstein",
        source_node_id=node_id,
        confidence=0.95,
    )

    assert candidate.candidate_type == "person"
    assert candidate.value == "Albert Einstein"
    assert candidate.source_node_id == node_id
    assert candidate.confidence == 0.95


def test_candidate_metadata():

    candidate = KnowledgeCandidate()

    candidate.add_metadata(
        "extractor",
        "entity_extractor",
    )

    assert candidate.metadata["extractor"] == "entity_extractor"