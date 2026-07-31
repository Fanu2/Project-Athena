import pytest

from athena.knowledge.acquisition.contracts.visitor import (
    Visitor,
)


def test_visitor_requires_implementation():

    with pytest.raises(TypeError):
        Visitor()