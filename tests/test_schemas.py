"""Tests for the fable boundary schemas (REQ-FABLE-0008, PDR-0006/0008)."""
import pytest
from pydantic import ValidationError

from fable.schemas import (
    ActionType,
    AgentActionProposal,
    Change,
    GMResolution,
    ResolutionSource,
    WorldStateDelta,
)


def test_valid_action_proposal_constructs() -> None:
    p = AgentActionProposal(
        agent_id="river_fam2_child",
        action_type=ActionType.ASK,
        target="river_fam2_parent_b",
        speech="If the medicine can save Mara, is it still wrong to keep it?",
    )
    assert p.action_type is ActionType.ASK
    assert p.agent_id == "river_fam2_child"


def test_action_type_outside_verb_set_is_rejected() -> None:
    with pytest.raises(ValidationError):
        AgentActionProposal(agent_id="a", action_type="teleport")


def test_proposals_forbid_unknown_fields() -> None:
    # extra=forbid guards against schema drift / typos crossing the boundary.
    with pytest.raises(ValidationError):
        AgentActionProposal(
            agent_id="a", action_type=ActionType.SPEAK, narration="I changed the world"  # type: ignore[call-arg]
        )


def test_world_state_delta_requires_a_typed_source() -> None:
    # An unknown source kind must be rejected (REQ-0001, determinism H5).
    with pytest.raises(ValidationError):
        WorldStateDelta(
            delta_id="d1",
            event_id="E1",
            source="narration",
            source_resolution_id="r1",
            changes=(Change(path="food.river", value=3),),
        )


def test_world_state_delta_requires_a_resolution_id() -> None:
    # No orphan deltas: source_resolution_id is mandatory.
    with pytest.raises(ValidationError):
        WorldStateDelta(  # type: ignore[call-arg]
            delta_id="d1",
            event_id="E1",
            source=ResolutionSource.AGENT,
            changes=(Change(path="food.river", value=3),),
        )


def test_changes_are_hashable_for_subset_checks() -> None:
    # The content-aware audit relies on Change being comparable as a set member.
    a = Change(path="food.river", value=3)
    b = Change(path="food.river", value=3)
    assert a == b
    assert len({a, b}) == 1


def test_gm_resolution_carries_sanctioned_changes() -> None:
    r = GMResolution(
        resolution_id="r1",
        action_id="act1",
        accepted=True,
        world_policy_id="wp-v1",
        sanctioned_changes=(Change(path="food.river", value=3),),
    )
    assert r.accepted is True
    assert r.sanctioned_changes[0].path == "food.river"
