"""
AEAF command line interface.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from ..config import AEAFConfig
from ..engine.pipeline import AnalysisPipeline
from ..reports.json_report import JSONReportGenerator
from ..reports.markdown import MarkdownReportGenerator
from ..reports.dashboard import DashboardBuilder


def audit_command(
    repository_path: Path,
) -> None:
    """
    Execute repository audit.
    """

    repository_path = repository_path.resolve()

    config = AEAFConfig.default(
        repository_path,
    )

    config.validate()

    pipeline = AnalysisPipeline(
        config,
    )

    repository = pipeline.run(
        repository_path,
    )

    stats = repository.statistics

    print()
    print("AEAF Audit")
    print("=" * 60)

    print(
        f"{'Source Files':20} {stats.source_files}"
    )

    print(
        f"{'Modules':20} {stats.modules}"
    )

    print(
        f"{'Classes':20} {stats.classes}"
    )

    print(
        f"{'Functions':20} {stats.functions}"
    )

    print(
        f"{'Methods':20} {stats.methods}"
    )

    print(
        f"{'Imports':20} {stats.imports}"
    )

    print(
        f"{'Dependencies':20} "
        f"{len(repository.dependency_graph.edges)}"
    )


    print()
    print("Generating Reports")
    print("-" * 60)


    report_directory = Path("reports")

    report_directory.mkdir(
        exist_ok=True,
    )


    json_path = (
        report_directory / "aeaf_report.json"
    )

    json_generator = JSONReportGenerator()

    json_generator.save(
        repository,
        json_path,
    )


    markdown_path = (
        report_directory / "aeaf_report.md"
    )

    markdown_generator = MarkdownReportGenerator()

    markdown_generator.save(
        repository,
        markdown_path,
    )


    dashboard_path = (
        report_directory / "aeaf_dashboard.html"
    )

    dashboard = DashboardBuilder()

    dashboard.build(
        repository,
        dashboard_path,
    )


    print(
        f"JSON       : {json_path}"
    )

    print(
        f"Markdown   : {markdown_path}"
    )

    print(
        f"Dashboard  : {dashboard_path}"
    )


    print()
    print("Audit complete.")


def main() -> None:
    """
    AEAF CLI entry point.
    """

    parser = argparse.ArgumentParser(
        prog="aeaf",
        description=(
            "Athena Engineering Audit Framework"
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )


    audit_parser = subparsers.add_parser(
        "audit",
        help="Audit a repository",
    )

    audit_parser.add_argument(
        "path",
        type=Path,
        help="Repository path",
    )


    args = parser.parse_args()


    if args.command == "audit":

        audit_command(
            args.path,
        )


if __name__ == "__main__":
    main()