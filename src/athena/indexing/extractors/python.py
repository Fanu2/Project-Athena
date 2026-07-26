"""
Python source code extractor.

Extracts Python source files into Athena ExtractedDocument format.
Adds lightweight structural information (classes, functions, imports)
before the original source text.
"""

from __future__ import annotations

import ast
from pathlib import Path

from athena.indexing.extractors.base import (
    BaseExtractor,
)
from athena.indexing.models import (
    ExtractedDocument,
    ExtractedPage,
)


class PythonExtractor(BaseExtractor):
    """Extractor for Python source files."""

    @property
    def supported_extensions(
        self,
    ) -> tuple[str, ...]:
        """Return supported extensions."""

        return (
            ".py",
        )

    def extract(
        self,
        document: Path,
    ) -> ExtractedDocument:
        """
        Extract Python source code.

        Adds structural information:
        - classes
        - functions
        - imports

        while preserving original source text.
        """

        source = document.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        classes: list[str] = []
        functions: list[str] = []
        imports: list[str] = []

        try:
            tree = ast.parse(
                source,
            )

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    ast.ClassDef,
                ):
                    classes.append(
                        node.name,
                    )

                elif isinstance(
                    node,
                    ast.FunctionDef,
                ):
                    functions.append(
                        node.name,
                    )

                elif isinstance(
                    node,
                    ast.AsyncFunctionDef,
                ):
                    functions.append(
                        node.name,
                    )

                elif isinstance(
                    node,
                    ast.Import,
                ):
                    for item in node.names:
                        imports.append(
                            item.name,
                        )

                elif isinstance(
                    node,
                    ast.ImportFrom,
                ):
                    if node.module:
                        imports.append(
                            node.module,
                        )

        except SyntaxError:
            # Keep source extraction working even
            # for incomplete Python files.
            pass

        structure = self._build_structure_header(
            document.name,
            classes,
            functions,
            imports,
        )

        enriched_text = (
            structure
            + "\n\n"
            + source
        )

        return ExtractedDocument(
            document_id=str(document.resolve()),
            path=document,
            title=document.stem,
            text=enriched_text,
            pages=(
                ExtractedPage(
                    page_number=1,
                    text=enriched_text,
                ),
            ),
            page_count=1,
        )

    @staticmethod
    def _build_structure_header(
        filename: str,
        classes: list[str],
        functions: list[str],
        imports: list[str],
    ) -> str:
        """Build searchable metadata header."""

        lines = [
            f"Python File: {filename}",
            "",
            "Classes:",
        ]

        if classes:
            lines.extend(
                f"- {item}"
                for item in classes
            )
        else:
            lines.append(
                "- None",
            )

        lines.extend(
            [
                "",
                "Functions:",
            ]
        )

        if functions:
            lines.extend(
                f"- {item}"
                for item in functions
            )
        else:
            lines.append(
                "- None",
            )

        lines.extend(
            [
                "",
                "Imports:",
            ]
        )

        if imports:
            lines.extend(
                f"- {item}"
                for item in sorted(set(imports))
            )
        else:
            lines.append(
                "- None",
            )

        return "\n".join(lines)