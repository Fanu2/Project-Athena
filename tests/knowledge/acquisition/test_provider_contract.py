import pytest

from athena.knowledge.acquisition.contracts.provider import (
    Provider,
)


def test_provider_requires_implementation():

    with pytest.raises(TypeError):
        Provider()