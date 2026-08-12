from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Mapping, Any
from uuid import uuid4


class IssueSeverity(IntEnum):
    INFO = 10
    WARNING = 20
    ERROR = 30
    CRITICAL = 40


@dataclass(frozen=True, slots=True)
class Issue:
    rule_id: str
    rule_name: str
    severity: IssueSeverity
    element_id: str
    message: str
    recommendation: str = ""
    issue_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.rule_id.strip():
            raise ValueError("rule_id es obligatorio")
        if not self.rule_name.strip():
            raise ValueError("rule_name es obligatorio")
        if not self.element_id.strip():
            raise ValueError("element_id es obligatorio")
        if not self.message.strip():
            raise ValueError("message es obligatorio")

    def to_dict(self) -> dict[str, Any]:
        return {
            "issue_id": self.issue_id,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "severity": self.severity.name,
            "element_id": self.element_id,
            "message": self.message,
            "recommendation": self.recommendation,
            "metadata": dict(self.metadata),
        }
