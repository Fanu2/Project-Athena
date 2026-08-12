"""
Assistant evidence adapter.
"""

from __future__ import annotations

from athena.domain.ai.evidence_record import (
    EvidenceRecord,
)

from .evidence_context import (
    AssistantEvidenceContext,
)


class AssistantEvidenceAdapter:
    """
    Converts evidence records into assistant context.
    """

    def build_context(
        self,
        records: list[EvidenceRecord],
    ) -> AssistantEvidenceContext:
        """
        Build assistant evidence context.
        """

        return AssistantEvidenceContext(
            records=tuple(records),
        )
