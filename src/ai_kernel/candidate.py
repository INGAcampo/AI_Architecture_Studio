from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping
from uuid import uuid4

class CandidateStatus(str, Enum):
    CREATED = "created"
    EVALUATED = "evaluated"
    REJECTED = "rejected"
    SELECTED = "selected"

@dataclass(frozen=True, slots=True)
class DesignCandidate:
    parameters: Mapping[str, Any]
    candidate_id: str = field(default_factory=lambda: str(uuid4()))
    generation: int = 0
    status: CandidateStatus = CandidateStatus.CREATED
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.generation < 0:
            raise ValueError("generation inválida")

    def with_status(self, status: CandidateStatus):
        return DesignCandidate(
            parameters=dict(self.parameters),
            candidate_id=self.candidate_id,
            generation=self.generation,
            status=status,
            metadata=dict(self.metadata),
        )
