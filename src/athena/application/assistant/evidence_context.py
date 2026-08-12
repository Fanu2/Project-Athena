"""
Assistant evidence context models.
"""

from __future__ import annotations

from dataclasses import dataclass

from athena.domain.ai.evidence_record import (
    EvidenceRecord,
)


@dataclass(frozen=True, slots=True)
class AssistantEvidenceContext:
    """
    Evidence available to assistant planning.
    """

    records: tuple[
        EvidenceRecord,
        ...
    ]
