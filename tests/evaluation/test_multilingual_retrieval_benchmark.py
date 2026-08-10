"""
Multilingual retrieval regression tests.
"""

from pathlib import Path

from athena.evaluation.benchmark_loader import BenchmarkLoader
from athena.evaluation.benchmark_validator import BenchmarkValidator


def test_multilingual_benchmark_dataset_valid():
    """
    Validate multilingual benchmark dataset.
    """

    dataset = Path(
        "tests/benchmarks/datasets/athena_multilingual_v1.json"
    )

    questions = BenchmarkLoader.load(
        str(dataset),
    )

    errors = BenchmarkValidator.validate(
        questions,
    )

    assert errors == []

    assert len(questions) == 9


def test_multilingual_expected_documents():
    """
    Ensure all multilingual documents are covered.
    """

    dataset = Path(
        "tests/benchmarks/datasets/athena_multilingual_v1.json"
    )

    questions = BenchmarkLoader.load(
        str(dataset),
    )

    expected = {
        question.expected_document_id
        for question in questions
    }

    assert expected == {
        "hindi_land_record",
        "punjabi_land_record",
        "french_land_record",
        "spanish_land_record",
        "assamese_land_record",
        "mizo_land_record",
        "english_architecture",
        "project_notes",
    }
