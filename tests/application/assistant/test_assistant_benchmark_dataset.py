"""
Tests for assistant benchmark dataset.
"""

from athena.application.assistant.benchmarks import (
    ASSISTANT_CORE_BENCHMARKS,
)


def test_core_benchmark_dataset_exists():

    assert len(
        ASSISTANT_CORE_BENCHMARKS
    ) == 5


def test_benchmark_cases_have_actions():

    for case in ASSISTANT_CORE_BENCHMARKS:

        assert case.name

        assert case.query

        assert case.expected_capability

        assert (
            len(case.expected_actions)
            > 0
        )
