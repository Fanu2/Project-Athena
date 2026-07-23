"""
AEAF domain models.

This module defines the core data structures shared across the entire
Athena Engineering Audit Framework (AEAF). Every pipeline stage enriches
a single RepositoryModel instance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum, auto
from pathlib import Path
from typing import Any


# ============================================================================
# Enums
# ============================================================================


class Severity(StrEnum):
    """Severity of an audit finding."""

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class FindingType(StrEnum):
    """Classification of an audit finding."""

    ARCHITECTURE = auto()
    DEPENDENCY = auto()
    COMPLEXITY = auto()
    DOCUMENTATION = auto()
    STYLE = auto()
    TESTING = auto()
    SECURITY = auto()
    PERFORMANCE = auto()


# ============================================================================
# Metadata
# ============================================================================


@dataclass(slots=True)
class RepositoryMetadata:
    """General repository information."""

    name: str = ""
    root: Path = Path()
    python_version: str = ""
    created_by: str = "AEAF"


@dataclass(slots=True)
class ProjectStatistics:
    """Repository statistics."""

    source_files: int = 0
    packages: int = 0
    modules: int = 0
    classes: int = 0
    functions: int = 0
    methods: int = 0
    imports: int = 0
    findings: int = 0


@dataclass(slots=True)
class ComplexityInfo:
    """
    Complexity information for a code element.
    """

    name: str

    kind: str

    score: int = 0

    details: dict[str, Any] = field(
        default_factory=dict,
    )


# ============================================================================
# Source Code Models
# ============================================================================


@dataclass(slots=True)
class SourceFile:
    path: Path
    module: str = ""
    package: str = ""


@dataclass(slots=True)
class ImportInfo:
    module: str
    name: str | None = None
    alias: str | None = None


@dataclass(slots=True)
class FunctionInfo:
    name: str
    lineno: int
    end_lineno: int | None = None
    parameters: list[str] = field(default_factory=list)
    decorators: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ClassInfo:
    name: str
    lineno: int
    end_lineno: int | None = None
    bases: list[str] = field(default_factory=list)
    methods: list[FunctionInfo] = field(default_factory=list)


@dataclass(slots=True)
class ModuleInfo:
    """
    Parsed Python module information.
    """

    name: str
    path: Path

    imports: list[ImportInfo] = field(default_factory=list)

    classes: list[ClassInfo] = field(
        default_factory=list,
    )

    functions: list[FunctionInfo] = field(
        default_factory=list,
    )

    dependencies: list[str] = field(
        default_factory=list,
    )

    dependents: list[str] = field(
        default_factory=list,
    )


@dataclass(slots=True)
class PackageInfo:
    name: str
    path: Path
    modules: list[ModuleInfo] = field(default_factory=list)


# ============================================================================
# Dependency Graph
# ============================================================================


@dataclass(slots=True)
class DependencyEdge:
    source: str
    target: str


@dataclass(slots=True)
class DependencyGraph:
    edges: list[DependencyEdge] = field(default_factory=list)


# ============================================================================
# Findings
# ============================================================================


@dataclass(slots=True)
class Finding:
    severity: Severity
    finding_type: FindingType
    message: str
    location: str = ""


@dataclass(slots=True)
class Recommendation:
    message: str


@dataclass(slots=True)
class PluginResult:
    plugin: str
    data: dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Root Repository Model
# ============================================================================


@dataclass(slots=True)
class RepositoryModel:
    """The central data model shared by the entire AEAF pipeline."""

    metadata: RepositoryMetadata = field(default_factory=RepositoryMetadata)
    statistics: ProjectStatistics = field(default_factory=ProjectStatistics)

    source_files: list[SourceFile] = field(default_factory=list)
    packages: list[PackageInfo] = field(default_factory=list)
    modules: list[ModuleInfo] = field(default_factory=list)

    dependency_graph: DependencyGraph = field(default_factory=DependencyGraph)

    complexity: list[ComplexityInfo] = field(
        default_factory=list,
    )

    findings: list[Finding] = field(default_factory=list)
    recommendations: list[Recommendation] = field(default_factory=list)
    plugin_results: list[PluginResult] = field(default_factory=list)