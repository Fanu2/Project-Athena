"""
Python AST parser.

Converts Python source code into AEAF domain models.

The parser enriches an existing RepositoryModel with information extracted
from Python Abstract Syntax Trees (AST). The parser performs no engineering
analysis—it only extracts structural information.
"""

from __future__ import annotations

import ast
from pathlib import Path

from ..config import AEAFConfig
from ..models import (
    ClassInfo,
    DocumentationInfo,
    FunctionInfo,
    ImportInfo,
    ModuleInfo,
    RepositoryModel,
)


class PythonASTParser:
    """
    Parse Python source files into RepositoryModel.
    """

    def __init__(self, config: AEAFConfig) -> None:
        """
        Initialize the parser.
        """

        self.config = config

    def parse(
        self,
        repository: RepositoryModel,
    ) -> RepositoryModel:
        """
        Parse every discovered Python source file.

        Parameters
        ----------
        repository
            Repository produced by RepositoryScanner.

        Returns
        -------
        RepositoryModel
            Repository enriched with module information.
        """

        repository.modules.clear()

        for source_file in repository.source_files:

            module = self._parse_module(
                source_file.path,
            )

            if module is not None:
                repository.modules.append(module)

        repository.statistics.modules = len(
            repository.modules
        )

        return repository

    def _parse_module(
        self,
        path: Path,
    ) -> ModuleInfo | None:
        """
        Parse a single Python module.
        """

        try:
            source = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            tree = ast.parse(
                source,
                filename=str(path),
            )

        except OSError:
            return None

        except SyntaxError:
            return None

        module = ModuleInfo(
            name=path.stem,
            path=path,
            documentation=self._extract_documentation(
                tree,
            ),
        )

        self._parse_tree(
            tree,
            module,
        )

        return module

    def _parse_tree(
        self,
        tree: ast.Module,
        module: ModuleInfo,
    ) -> None:
        """
        Parse a module AST.

        This method coordinates the extraction process.
        Each parser is responsible for one aspect of the AST.
        """

        self._parse_imports(
            tree,
            module,
        )

        self._parse_classes(
            tree,
            module,
        )

        self._parse_functions(
            tree,
            module,
        )

    def _parse_imports(
        self,
        tree: ast.Module,
        module: ModuleInfo,
    ) -> None:
        """
        Extract import statements from a module.
        """

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:

                    module.imports.append(
                        ImportInfo(
                            module=alias.name,
                            alias=alias.asname,
                        )
                    )

            elif isinstance(node, ast.ImportFrom):

                module_name = node.module or ""

                for alias in node.names:

                    module.imports.append(
                        ImportInfo(
                            module=module_name,
                            name=alias.name,
                            alias=alias.asname,
                        )
                    )

    def _parse_classes(
        self,
        tree: ast.Module,
        module: ModuleInfo,
    ) -> None:
        """
        Extract top-level class definitions.
        """

        for node in tree.body:

            if not isinstance(node, ast.ClassDef):
                continue

            class_info = ClassInfo(
                name=node.name,
                lineno=node.lineno,
                end_lineno=getattr(
                    node,
                    "end_lineno",
                    None,
                ),
                bases=self._extract_base_classes(
                    node,
                ),
                documentation=self._extract_documentation(
                    node,
                ),
            )

            self._parse_methods(
                node,
                class_info,
            )

            module.classes.append(
                class_info,
            )

    def _parse_methods(
        self,
        class_node: ast.ClassDef,
        class_info: ClassInfo,
    ) -> None:
        """
        Extract methods from a class.
        """

        for node in class_node.body:

            if not isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                continue

            method = FunctionInfo(
                name=node.name,
                lineno=node.lineno,
                end_lineno=getattr(
                    node,
                    "end_lineno",
                    None,
                ),
                parameters=self._extract_parameters(
                    node,
                ),
                decorators=self._extract_decorators(
                    node,
                ),
                documentation=self._extract_documentation(
                    node,
                ),
            )

            class_info.methods.append(
                method,
            )

    def _parse_functions(
        self,
        tree: ast.Module,
        module: ModuleInfo,
    ) -> None:
        """
        Extract top-level functions.

        Methods belonging to classes are handled separately by
        `_parse_methods()`.
        """

        for node in tree.body:

            if not isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                ),
            ):
                continue

            function = FunctionInfo(
                name=node.name,
                lineno=node.lineno,
                end_lineno=getattr(
                    node,
                    "end_lineno",
                    None,
                ),
                parameters=self._extract_parameters(
                    node,
                ),
                decorators=self._extract_decorators(
                    node,
                ),
                documentation=self._extract_documentation(
                    node,
                ),
            )

            module.functions.append(
                function,
            )

    def _extract_base_classes(
        self,
        node: ast.ClassDef,
    ) -> list[str]:
        """
        Extract base class names.
        """

        bases: list[str] = []

        for base in node.bases:

            if isinstance(base, ast.Name):

                bases.append(base.id)

            elif isinstance(base, ast.Attribute):

                parts: list[str] = []

                current = base

                while isinstance(current, ast.Attribute):
                    parts.append(current.attr)
                    current = current.value

                if isinstance(current, ast.Name):
                    parts.append(current.id)

                bases.append(".".join(reversed(parts)))

            else:

                try:
                    bases.append(ast.unparse(base))
                except Exception:
                    bases.append("<unknown>")

        return bases

    def _extract_parameters(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> list[str]:
        """
        Extract function or method parameters.
        """

        parameters: list[str] = []

        # Positional-only parameters (Python 3.8+)
        for arg in node.args.posonlyargs:
            parameters.append(arg.arg)

        # Positional or keyword parameters
        for arg in node.args.args:
            parameters.append(arg.arg)

        # *args
        if node.args.vararg:
            parameters.append("*" + node.args.vararg.arg)

        # Keyword-only parameters
        for arg in node.args.kwonlyargs:
            parameters.append(arg.arg)

        # **kwargs
        if node.args.kwarg:
            parameters.append("**" + node.args.kwarg.arg)

        return parameters

    def _extract_decorators(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> list[str]:
        """
        Extract decorators from a function or method.
        """

        decorators: list[str] = []

        for decorator in node.decorator_list:

            try:
                decorators.append(
                    ast.unparse(decorator)
                )
            except Exception:
                decorators.append("<unknown>")

        return decorators

    def _extract_documentation(
        self,
        node,
    ) -> DocumentationInfo:
        """
        Extract documentation information from AST node.
        """

        docstring = ast.get_docstring(
            node,
        )

        if not docstring:
            return DocumentationInfo()

        summary = docstring.strip().splitlines()[0]

        return DocumentationInfo(
            has_docstring=True,
            summary=summary,
        )