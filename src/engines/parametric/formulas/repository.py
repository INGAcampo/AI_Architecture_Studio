from __future__ import annotations

from .model import FormulaDefinition


class FormulaRepository:
    def __init__(self) -> None:
        self._formulas: dict[str, FormulaDefinition] = {}
        self.revision = 0

    def add(self, formula: FormulaDefinition, *, replace: bool = False) -> None:
        if formula.formula_id in self._formulas and not replace:
            raise KeyError(f"Fórmula ya existente: {formula.formula_id}")
        self._formulas[formula.formula_id] = formula
        self.revision += 1

    def get(self, formula_id: str) -> FormulaDefinition:
        try:
            return self._formulas[formula_id]
        except KeyError as exc:
            raise KeyError(f"Fórmula desconocida: {formula_id}") from exc

    def remove(self, formula_id: str) -> FormulaDefinition:
        formula = self.get(formula_id)
        self._formulas.pop(formula_id)
        self.revision += 1
        return formula

    def all(self) -> tuple[FormulaDefinition, ...]:
        return tuple(self._formulas[key] for key in sorted(self._formulas))

    def for_owner(self, owner_id: str) -> tuple[FormulaDefinition, ...]:
        return tuple(formula for formula in self.all() if formula.owner_id == owner_id)

    def by_target(self, owner_id: str, target_parameter: str) -> FormulaDefinition | None:
        return next(
            (
                formula
                for formula in self._formulas.values()
                if formula.owner_id == owner_id
                and formula.target_parameter == target_parameter
            ),
            None,
        )
