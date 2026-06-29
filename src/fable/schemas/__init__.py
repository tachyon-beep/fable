"""fable boundary schemas (REQ-FABLE-0008).

Versioned pydantic models validated at every boundary. This package will grow to the full
nine I/O schemas (observation, action, resolution/delta, memory, reflection, evaluation,
manifest) plus the content-hash-pinned config artifacts (PDR-0007).
"""
from .action import ActionType, AgentActionProposal
from .base import FableModel
from .world import Change, GMResolution, ResolutionSource, WorldStateDelta

__all__ = [
    "ActionType",
    "AgentActionProposal",
    "Change",
    "FableModel",
    "GMResolution",
    "ResolutionSource",
    "WorldStateDelta",
]
