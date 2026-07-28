from athena.evaluation.benchmark_models import BenchmarkQuestion
from athena.evaluation.benchmark_validator import BenchmarkValidator


def test_empty_dataset():
    assert BenchmarkValidator.validate([])


def test_valid_dataset():
    questions = [
        BenchmarkQuestion(
            question_id="Q1",
            question="What is Athena?",
        )
    ]

    assert BenchmarkValidator.validate(questions) == []


def test_duplicate_question_id():
    questions = [
        BenchmarkQuestion("Q1", "Question A"),
        BenchmarkQuestion("Q1", "Question B"),
    ]

    errors = BenchmarkValidator.validate(questions)

    assert any("Duplicate question_id" in e for e in errors)


def test_duplicate_question_text():
    questions = [
        BenchmarkQuestion("Q1", "Question"),
        BenchmarkQuestion("Q2", "Question"),
    ]

    errors = BenchmarkValidator.validate(questions)

    assert any("Duplicate question text" in e for e in errors)


def test_blank_question():
    questions = [
        BenchmarkQuestion(
            question_id="Q1",
            question="",
        )
    ]

    errors = BenchmarkValidator.validate(questions)

    assert any("empty question" in e for e in errors)


def test_blank_question_id():
    questions = [
        BenchmarkQuestion(
            question_id="",
            question="Hello",
        )
    ]

    errors = BenchmarkValidator.validate(questions)

    assert any("empty question_id" in e for e in errors)

