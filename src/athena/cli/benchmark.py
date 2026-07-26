"""
Athena Benchmark CLI.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from athena.core.application_context import ApplicationContext
from athena.evaluation.benchmark_service import BenchmarkService


def load_suite(
    path: str,
) -> list[str]:
    """Load benchmark datasets from a suite file."""

    suite_path = Path(path)

    with suite_path.open(
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    base_path = suite_path.parent

    return [str(base_path / dataset["path"]) for dataset in data["datasets"]]


def main() -> None:
    """Benchmark command-line entry point."""

    parser = argparse.ArgumentParser(
        prog="athena-benchmark",
        description="Athena Retrieval Benchmark",
    )

    parser.add_argument(
        "--workspace",
        required=True,
        help="Athena workspace path",
    )

    parser.add_argument(
        "--dataset",
        required=False,
        help="Benchmark dataset JSON file",
    )

    parser.add_argument(
        "--suite",
        required=False,
        help="Benchmark suite JSON file",
    )

    args = parser.parse_args()

    if not args.dataset and not args.suite:
        raise ValueError(
            "Provide either --dataset or --suite.",
        )

    print("=" * 60)
    print("Athena Retrieval Benchmark")
    print("=" * 60)

    context = ApplicationContext()

    try:
        context.open_workspace(
            Path(args.workspace),
        )

        if context.retrieval_service is None:
            raise RuntimeError(
                "Retrieval service was not initialized.",
            )

        service = BenchmarkService(
            context.retrieval_service,
        )

        if args.suite:
            datasets = load_suite(
                args.suite,
            )

            print()
            print(
                f"Benchmark Suite: {args.suite}",
            )

            for dataset in datasets:
                print()
                print(
                    f"Running benchmark: {dataset}",
                )

                service.run(
                    dataset,
                )

        else:
            service.run(
                args.dataset,
            )

        print()
        print("Benchmark completed successfully.")

    finally:
        context.close_workspace()


if __name__ == "__main__":
    main()
