"""World-state change schemas (REQ-FABLE-0001/0004/0013, PDR-0005/0008).

The world changes ONLY by applying a `WorldStateDelta`, and a delta may exist only as the
product of a `GMResolution`. A delta carries a TYPED source (agent vs system/environmental)
and a mandatory `source_resolution_id` — there are no orphan deltas. The resolution records
the changes it sanctioned, so the audit can check delta content against sanction (not just a
non-null pointer).
"""
from enum import StrEnum

from .base import FableModel

JsonScalar = str | int | float | bool | None


class ResolutionSource(StrEnum):
    AGENT = "agent_resolution"
    SYSTEM = "system_resolution"  # environmental world-update (e.g. weather, scarcity)


class Change(FableModel):
    """One atomic world-state change: a dotted state path and its new scalar value."""

    path: str
    value: JsonScalar


class GMResolution(FableModel):
    schema_version: int = 1
    resolution_id: str
    action_id: str | None  # None for system/environmental resolutions
    accepted: bool
    rejection_reason: str | None = None
    world_policy_id: str
    sanctioned_changes: tuple[Change, ...] = ()


class WorldStateDelta(FableModel):
    schema_version: int = 1
    delta_id: str
    event_id: str
    source: ResolutionSource
    source_resolution_id: str
    changes: tuple[Change, ...]
