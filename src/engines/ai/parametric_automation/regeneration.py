from __future__ import annotations
from dataclasses import dataclass

from .dependency_graph import DependencyGraph
from .formula import Formula
from .model import ParameterSet


@dataclass(frozen=True, slots=True)
class RegenerationReport:
    changed_parameters: tuple[str, ...]
    evaluated_formulas: tuple[str, ...]
    errors: tuple[str, ...]
    revision_before: int
    revision_after: int

    @property
    def success(self) -> bool:
        return not self.errors


class RegenerationService:
    def __init__(self) -> None:
        self._formulas: dict[str, Formula] = {}
        self._graph = DependencyGraph()

    def register_formula(self, formula: Formula) -> None:
        target = formula.target_parameter_id
        if target in self._formulas:
            raise ValueError(f"Fórmula duplicada para {target}")
        self._formulas[target] = formula
        self._graph.add_node(target)
        for dependency in formula.dependencies():
            self._graph.add_dependency(target, dependency)

    def formula(self, parameter_id: str) -> Formula:
        return self._formulas[parameter_id]

    def affected_parameters(self, parameter_id: str) -> tuple[str, ...]:
        return tuple(
            node
            for node in self._graph.affected_by(parameter_id)
            if node in self._formulas
        )

    def regenerate(
        self,
        parameters: ParameterSet,
        *,
        changed_parameter_ids: tuple[str, ...] | None = None,
    ) -> RegenerationReport:
        revision_before = parameters.revision
        changed = []
        evaluated = []
        errors = []

        if changed_parameter_ids:
            targets = set()
            for parameter_id in changed_parameter_ids:
                targets.update(self.affected_parameters(parameter_id))
        else:
            targets = set(self._formulas)

        values = parameters.values()
        order = self._graph.topological_order()

        for parameter_id in order:
            if parameter_id not in targets:
                continue
            formula = self._formulas.get(parameter_id)
            if formula is None:
                continue
            try:
                result = formula.evaluate(values)
                evaluated.append(parameter_id)
                if parameters.set(parameter_id, result, source="formula"):
                    changed.append(parameter_id)
                    values[parameter_id] = parameters.get(parameter_id)
            except Exception as exc:
                errors.append(f"{parameter_id}: {exc}")

        return RegenerationReport(
            changed_parameters=tuple(changed),
            evaluated_formulas=tuple(evaluated),
            errors=tuple(errors),
            revision_before=revision_before,
            revision_after=parameters.revision,
        )
