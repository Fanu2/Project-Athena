import pytest

from athena.knowledge.acquisition.contracts.importer import (
    Importer,
)


def test_importer_requires_implementation():

    with pytest.raises(TypeError):
        Importer()