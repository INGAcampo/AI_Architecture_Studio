from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class ResponseKind(str, Enum):
    ANSWER = "answer"
    ACTION_RESULT = "action_result"
    ERROR = "error"
    SUGGESTION = "suggestion"


@dataclass(frozen=True, slots=True)
class AssistantResponse:
    text: str
    kind: ResponseKind = ResponseKind.ANSWER
    data: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("text es obligatorio")
