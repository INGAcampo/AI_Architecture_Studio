from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class IntentType(str, Enum):
    QUERY_SELECTION = "query_selection"
    QUERY_COUNTS = "query_counts"
    QUERY_ISSUES = "query_issues"
    QUERY_CONTEXT = "query_context"
    MODIFY_PROPERTY = "modify_property"
    RUN_RULES = "run_rules"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class AssistantIntent:
    intent_type: IntentType
    confidence: float
    entities: Mapping[str, Any] = field(default_factory=dict)
    raw_prompt: str = ""

    def __post_init__(self) -> None:
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence debe estar entre 0 y 1")
