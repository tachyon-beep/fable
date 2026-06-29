"""Agent action interface (REQ-FABLE-0002): a fixed, versioned verb set.

Agents act ONLY by emitting an `AgentActionProposal` whose `action_type` is in this set.
Free-form narration is not an action — it cannot change the world (REQ-FABLE-0001).
"""
from enum import StrEnum

from .base import FableModel


class ActionType(StrEnum):
    OBSERVE = "observe"
    SPEAK = "speak"
    ASK = "ask"
    GIVE = "give"
    TAKE = "take"
    HIDE = "hide"
    ACCUSE = "accuse"
    DEFEND = "defend"
    PUNISH = "punish"
    FORGIVE = "forgive"
    TRADE = "trade"
    TEACH_CHILD = "teach_child"
    FAMILY_REFLECT = "family_reflect"
    COUNCIL_VOTE = "council_vote"
    PRIVATE_REFLECT = "private_reflect"
    RITUALISE = "ritualise"


class AgentActionProposal(FableModel):
    schema_version: int = 1
    agent_id: str
    action_type: ActionType
    target: str | None = None
    object: str | None = None
    speech: str | None = None
    private_reasoning_summary: str | None = None
