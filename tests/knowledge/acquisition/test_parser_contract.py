import pytest

from athena.knowledge.acquisition.contracts.parser import (
    Parser,
)


def test_parser_requires_implementation():

    with pytest.raises(TypeError):
        Parser()