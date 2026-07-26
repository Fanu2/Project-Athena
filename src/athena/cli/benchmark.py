"""
Athena Benchmark CLI.
"""

from __future__ import annotations

import argparse

from athena.evaluation.benchmark_loader import BenchmarkLoader


def main() -> None:
    """Benchmark command-line entry point."""

    parser = argparse.ArgumentParser(
        prog="athena-benchmark",
        description="Athena Retrieval Benchmark",
    )

    parser.add_argument(
        "--dataset",
        required=True,
        help="Benchmark dataset JSON file",
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Athena Retrieval Benchmark")
    print("=" * 60)

    questions = BenchmarkLoader.load(args.dataset)

    print(f"Dataset : {args.dataset}")
    print(f"Questions Loaded : {len(questions)}")
    print()

    for question in questions:
        print(f"{question.question_id}: {question.question}")

    print()
    print("Loader verification completed successfully.")


if __name__ == "__main__":
    main()
