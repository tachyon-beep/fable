"""Tests for the content-aware zero-hallucination audit (REQ-FABLE-0001, PDR-0008).

The audit enforces that the world only changes through the GM: every WorldStateDelta must
(a) reference a known resolution (no orphans), and (b) carry only changes that its resolution
actually sanctioned (content-aware, not just a non-null pointer).
"""
from fable.audit import AuditFindingKind, audit_deltas
from fable.schemas import Change, GMResolution, ResolutionSource, WorldStateDelta


def _resolution(rid: str, *changes: Change, action_id: str | None = "act") -> GMResolution:
    return GMResolution(
        resolution_id=rid,
        action_id=action_id,
        accepted=True,
        world_policy_id="wp-v1",
        sanctioned_changes=tuple(changes),
    )


def _delta(
    rid: str, *changes: Change, source: ResolutionSource = ResolutionSource.AGENT
) -> WorldStateDelta:
    return WorldStateDelta(
        delta_id=f"d-{rid}",
        event_id="E1",
        source=source,
        source_resolution_id=rid,
        changes=tuple(changes),
    )


def test_clean_delta_passes() -> None:
    c = Change(path="food.river", value=3)
    findings = audit_deltas([_resolution("r1", c)], [_delta("r1", c)])
    assert findings == []


def test_unsanctioned_change_is_flagged_as_hallucination() -> None:
    sanctioned = Change(path="food.river", value=3)
    smuggled = Change(path="leader.river", value="me")  # never sanctioned by the resolution
    findings = audit_deltas([_resolution("r1", sanctioned)], [_delta("r1", sanctioned, smuggled)])
    assert len(findings) == 1
    assert findings[0].kind is AuditFindingKind.UNSANCTIONED_CHANGE
    assert findings[0].delta_id == "d-r1"


def test_orphan_delta_is_flagged() -> None:
    c = Change(path="food.river", value=3)
    # delta references r-missing, but only r1 exists
    findings = audit_deltas([_resolution("r1", c)], [_delta("r-missing", c)])
    assert len(findings) == 1
    assert findings[0].kind is AuditFindingKind.ORPHAN


def test_system_resolution_delta_is_audited_like_any_other() -> None:
    # Environmental (system_resolution) deltas must still be sanctioned by a resolution.
    c = Change(path="weather.day", value="drought")
    sys_res = _resolution("sys1", c, action_id=None)
    findings = audit_deltas([sys_res], [_delta("sys1", c, source=ResolutionSource.SYSTEM)])
    assert findings == []


def test_multiple_deltas_report_independently() -> None:
    c1 = Change(path="food.river", value=3)
    c2 = Change(path="food.stone", value=2)
    bad = Change(path="reputation.x", value=-1)
    findings = audit_deltas(
        [_resolution("r1", c1), _resolution("r2", c2)],
        [_delta("r1", c1), _delta("r2", c2, bad)],
    )
    assert len(findings) == 1
    assert findings[0].delta_id == "d-r2"
    assert findings[0].kind is AuditFindingKind.UNSANCTIONED_CHANGE
