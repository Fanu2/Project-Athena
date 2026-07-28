"""
Document authority ranking.

Provides a ranking signal based on document role and type.
"""

from __future__ import annotations


class DocumentAuthorityRanker:
    """Calculate authority score for a document."""

    def score(
        self,
        document_name: str,
        document_path: str = "",
    ) -> float:
        """Return document authority score."""

        name = document_name.lower()
        path = document_path.lower()

        value = f"{path}/{name}"

        if (
            "/code/" in value
            or "\\code\\" in value
            or value.endswith(".py")
        ):
            return 0.0

        if any(
            term in name
            for term in [
                "constitution",
                "specification",
                "architecture",
                "adr",
                "design",
            ]
        ):
            return 0.20

        if any(
            term in name
            for term in [
                "guide",
                "manual",
                "documentation",
                "readme",
            ]
        ):
            return 0.15

        if name.endswith(".md"):
            return 0.10

        if name.endswith((".docx", ".pdf")):
            return 0.08

        return 0.0
