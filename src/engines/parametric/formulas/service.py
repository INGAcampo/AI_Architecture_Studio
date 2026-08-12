from __future__ import annotations

from .engine import FormulaEngine
from .model import FormulaDefinition


class FormulaService:
    def __init__(self, engine: FormulaEngine) -> None:
        self.engine = engine

    def define(
        self,
        formula_id: str,
        owner_id: str,
        target_parameter: str,
        expression: str,
        *,
        replace: bool = False,
    ) -> FormulaDefinition:
        formula = FormulaDefinition(
            formula_id=formula_id,
            owner_id=owner_id,
            target_parameter=target_parameter,
            expression=expression,
        )
        self.engine.add_formula(formula, replace=replace)
        return formula

    def recalculate(self, owner_id: str):
        return self.engine.evaluate_owner(owner_id)

    def parameter_changed(self, owner_id: str, parameter_id: str):
        return self.engine.propagate(owner_id, parameter_id)
