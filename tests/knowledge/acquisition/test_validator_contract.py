import pytest

from athena.knowledge.acquisition.contracts.validator import (
    Validator,
)


def test_validator_requires_implementation():

    with pytest.raises(TypeError):
        Validator()