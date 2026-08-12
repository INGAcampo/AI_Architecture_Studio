from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FormulaStatus(str, Enum):
    READY = "ready"
    EVALUATED = "evaluated"
    ERROR = "error"
    DISABLED = "disabled"


@dataclass(slots=True)
class FormulaDefinition:
    formula_id: str
    owner_id: str
    target_parameter: str
    expression: str
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
    status: FormulaStatus = FormulaStatus.READY
    error: str | None = None
    revision: int = 0

    def __post_init__(self) -> None:
        if not self.formula_id.strip():
            raise ValueError("formula_id no puede estar vacío")
        if not self.owner_id.strip():
            raise ValueError("owner_id no puede estar vacío")
        if not self.target_parameter.strip():
            raise ValueError("target_parameter no puede estar vacío")
        if not self.expression.strip():
            raise ValueError("expression no puede estar vacía")
