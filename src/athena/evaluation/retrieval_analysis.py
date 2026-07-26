"""
Retrieval analysis models.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RetrievalIssueType(str, Enum):
    """Retrieval issue categories."""

    DUPLICATE_DOCUMENT = "duplicate_document"
    WRONG_RANK = "wrong_rank"
    NOT_RETRIEVED = "not_retrieved"
    DOCUMENT_OVERLAP = "document_overlap"


@dataclass(slots=True, frozen=True)
class RetrievalFinding:
    """A retrieval improvement finding."""

    question_id: str

    issue_type: RetrievalIssueType

    expected_document: str

    retrieved_documents: list[str]

    description: str


@dataclass(slots=True)
class RetrievalAnalysisReport:
    """Collection of retrieval findings."""

    findings: list[RetrievalFinding]

    @property
    def total_findings(self) -> int:
        """Return finding count."""

        return len(self.findings)
