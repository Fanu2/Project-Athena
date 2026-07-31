import pytest

from athena.knowledge.acquisition.contracts.pipeline_stage import (
    PipelineStage,
)


def test_pipeline_stage_requires_implementation():

    with pytest.raises(TypeError):
        PipelineStage()