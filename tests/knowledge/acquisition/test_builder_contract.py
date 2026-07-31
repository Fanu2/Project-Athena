import pytest

from athena.knowledge.acquisition.contracts.builder import (
    Builder,
)


def test_builder_requires_implementation():

    with pytest.raises(TypeError):
        Builder()