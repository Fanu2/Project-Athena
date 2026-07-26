"""
Athena Benchmark CLI.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from athena.core.application_context import ApplicationContext
from athena.evaluation.benchmark_service import BenchmarkService


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
        required=True,
        help="Benchmark dataset JSON file",
    )

    args = parser.parse_args()

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

        service.run(
            args.dataset,
        )

        print()
        print("Benchmark completed successfully.")

    finally:
        context.close_workspace()


if __name__ == "__main__":
    main()
