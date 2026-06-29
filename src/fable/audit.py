"""Content-aware zero-hallucination audit (REQ-FABLE-0001, PDR-0008).

This is the Stage-0 exit gate. The no-narration invariant is enforced mechanically, not by
convention: every `WorldStateDelta` must reference a known `GMResolution` (no orphans), and a
delta may carry ONLY changes that its resolution actually sanctioned. Checking content (the set
of changes) — not merely a non-null pointer — is what stops a hallucinated mutation that cites a
real resolution id from slipping through.
"""
from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum

from .schemas import GMResolution, WorldStateDelta


class AuditFindingKind(StrEnum):
    ORPHAN = "orphan"
    UNSANCTIONED_CHANGE = "unsanctioned_change"


@dataclass(frozen=True)
class AuditFinding:
    delta_id: str
    kind: AuditFindingKind
    detail: str


def audit_deltas(
    resolutions: Iterable[GMResolution],
    deltas: Iterable[WorldStateDelta],
) -> list[AuditFinding]:
    """Return findings for any delta that is unsourced or carries unsanctioned changes.

    An empty list means clean — every delta traces to a resolution and every change in every
    delta was sanctioned by that resolution.
    """
    by_id = {r.resolution_id: r for r in resolutions}
    findings: list[AuditFinding] = []
    for delta in deltas:
        resolution = by_id.get(delta.source_resolution_id)
        if resolution is None:
            findings.append(
                AuditFinding(
                    delta_id=delta.delta_id,
                    kind=AuditFindingKind.ORPHAN,
                    detail=f"delta references unknown resolution {delta.source_resolution_id!r}",
                )
            )
            continue
        sanctioned = set(resolution.sanctioned_changes)
        unsanctioned = [c for c in delta.changes if c not in sanctioned]
        if unsanctioned:
            paths = ", ".join(c.path for c in unsanctioned)
            findings.append(
                AuditFinding(
                    delta_id=delta.delta_id,
                    kind=AuditFindingKind.UNSANCTIONED_CHANGE,
                    detail=(
                        f"delta carries changes not sanctioned by "
                        f"{resolution.resolution_id}: {paths}"
                    ),
                )
            )
    return findings
