from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class ActionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True, slots=True)
class AssistantAction:
    action_id: str
    action_type: str
    payload: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.action_id.strip():
            raise ValueError("action_id es obligatorio")
        if not self.action_type.strip():
            raise ValueError("action_type es obligatorio")
