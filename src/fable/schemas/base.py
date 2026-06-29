"""Base for all fable boundary schemas.

Frozen + extra-forbidden: frozen makes instances hashable (the audit relies on set
membership of `Change`) and immutable (determinism), and forbidding extra fields stops
schema drift or a typo'd field from silently crossing a boundary (REQ-FABLE-0008).
"""
from pydantic import BaseModel, ConfigDict


class FableModel(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
