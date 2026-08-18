from dataclasses import dataclass, field
from typing import Any, Mapping

@dataclass(frozen=True, slots=True)
class EvaluationContext:
    project_id: str
    discipline: str = "multidisciplinary"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.project_id.strip():
            raise ValueError("project_id es obligatorio")
