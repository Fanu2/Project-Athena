import pytest

from athena.knowledge.acquisition.contracts.extractor import (
    Extractor,
)


def test_extractor_requires_implementation():

    with pytest.raises(TypeError):
        Extractor()