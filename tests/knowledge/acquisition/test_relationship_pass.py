"""
Relationship Pass tests.
"""

from athena.knowledge.acquisition.pipeline.relationship_pass import (
    RelationshipPass,
)

from athena.knowledge.acquisition.domain.knowledge_context import (
    KnowledgeContext,
)

from athena.knowledge.acquisition.domain.knowledge_candidate import (
    KnowledgeCandidate,
)


def test_relationship_pass_creates_candidate_relationship():

    context = KnowledgeContext()

    first = KnowledgeCandidate(
        value="Athena",
    )

    second = KnowledgeCandidate(
        value="Knowledge",
    )

    result = RelationshipPass().execute(
        context,
        [
            first,
            second,
        ],
    )

    #
    # Main compiler stream is preserved
    #

    assert len(result) == 2

    #
    # Relationship side output exists
    #

    relationships = (
        context.get_metadata(
            "candidate_relationships"
        )
    )

    assert relationships is not None

    assert len(relationships) == 1

    relationship = relationships[0]

    assert (
        relationship.source_candidate_id
        == first.candidate_id
    )

    assert (
        relationship.target_candidate_id
        == second.candidate_id
    )