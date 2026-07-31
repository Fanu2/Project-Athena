import pytest

from athena.knowledge.acquisition.contracts.relationship_extractor import (
    RelationshipExtractor,
)


def test_relationship_extractor_requires_implementation():

    with pytest.raises(TypeError):
        RelationshipExtractor()