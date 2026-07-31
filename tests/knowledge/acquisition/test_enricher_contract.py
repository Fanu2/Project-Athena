import pytest

from athena.knowledge.acquisition.contracts.enricher import (
    Enricher,
)


def test_enricher_requires_implementation():

    with pytest.raises(TypeError):
        Enricher()