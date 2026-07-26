"""
Temporary workspace re-index utility.

Used after extractor/indexing changes.
"""

from __future__ import annotations

from pathlib import Path

from athena.core.application_context import ApplicationContext


WORKSPACE = Path(
    r"C:\Users\singh\Videos\AthenaBenchmarkWorkspace"
)


def main() -> None:
    """Force re-index all workspace documents."""

    context = ApplicationContext()

    try:
        context.open_workspace(
            WORKSPACE,
        )

        documents_folder = (
            WORKSPACE / "documents"
        )

        print(
            f"Re-indexing: {documents_folder}"
        )

        count = 0

        for document in documents_folder.rglob("*"):
            if document.is_file():

                context.indexing_service.index_document(
                    document,
                    force=True,
                )

                count += 1

        print(
            f"Re-indexed files: {count}"
        )

    finally:
        context.close_workspace()


if __name__ == "__main__":
    main()