from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .ast_tools import ParsedFormula, SafeFormulaParser
from .graph import ParameterDependencyGraph
from .model import FormulaDefinition, FormulaStatus
from .repository import FormulaRepository


@dataclass(frozen=True, slots=True)
class FormulaEvaluation:
    formula_id: str
    owner_id: str
    target_parameter: str
    value: Any
    dependencies: tuple[str, ...]
    success: bool
    error: str | None = None


class FormulaEngine:
    def __init__(
        self,
        parameter_engine,
        *,
        parser: SafeFormulaParser | None = None,
        repository: FormulaRepository | None = None,
        graph: ParameterDependencyGraph | None = None,
        event_dispatcher=None,
    ) -> None:
        self.parameter_engine = parameter_engine
        self.parser = parser or SafeFormulaParser()
        self.repository = repository or FormulaRepository()
        self.graph = graph or ParameterDependencyGraph()
        self.event_dispatcher = event_dispatcher
        self._parsed: dict[str, ParsedFormula] = {}

    @staticmethod
    def node_id(owner_id: str, parameter_id: str) -> str:
        return f"{owner_id}:{parameter_id}"

    def add_formula(self, formula: FormulaDefinition, *, replace: bool = False) -> None:
        parsed = self.parser.parse(formula.expression)
        target_node = self.node_id(formula.owner_id, formula.target_parameter)
        self.graph.add_node(target_node)

        added_edges: list[tuple[str, str]] = []
        try:
            for dependency in parsed.dependencies:
                source_node = self.node_id(formula.owner_id, dependency)
                self.graph.add_dependency(source_node, target_node)
                added_edges.append((source_node, target_node))
            self.repository.add(formula, replace=replace)
            self._parsed[formula.formula_id] = parsed
        except Exception:
            for source, target in added_edges:
                self.graph.remove_dependency(source, target)
            raise

        self._publish(
            "formula.added",
            formula_id=formula.formula_id,
            owner_id=formula.owner_id,
            target_parameter=formula.target_parameter,
        )

    def remove_formula(self, formula_id: str) -> FormulaDefinition:
        formula = self.repository.remove(formula_id)
        parsed = self._parsed.pop(formula_id)
        target_node = self.node_id(formula.owner_id, formula.target_parameter)
        for dependency in parsed.dependencies:
            self.graph.remove_dependency(
                self.node_id(formula.owner_id, dependency),
                target_node,
            )
        self._publish("formula.removed", formula_id=formula_id)
        return formula

    def evaluate(self, formula_id: str) -> FormulaEvaluation:
        formula = self.repository.get(formula_id)
        if not formula.enabled:
            formula.status = FormulaStatus.DISABLED
            return FormulaEvaluation(
                formula.formula_id,
                formula.owner_id,
                formula.target_parameter,
                None,
                (),
                False,
                "Fórmula deshabilitada",
            )

        parsed = self._parsed[formula_id]

        try:
            collection = self.parameter_engine.get_collection(formula.owner_id)
            values = {
                dependency: collection.value(dependency)
                for dependency in parsed.dependencies
            }
            value = self.parser.evaluate(parsed, values)
            self.parameter_engine.set_calculated(
                formula.owner_id,
                formula.target_parameter,
                value,
                source=f"formula:{formula.formula_id}",
            )
            formula.status = FormulaStatus.EVALUATED
            formula.error = None
            formula.revision += 1
            result = FormulaEvaluation(
                formula.formula_id,
                formula.owner_id,
                formula.target_parameter,
                value,
                parsed.dependencies,
                True,
            )
        except Exception as exc:
            formula.status = FormulaStatus.ERROR
            formula.error = str(exc)
            result = FormulaEvaluation(
                formula.formula_id,
                formula.owner_id,
                formula.target_parameter,
                None,
                parsed.dependencies,
                False,
                str(exc),
            )

        self._publish(
            "formula.evaluated",
            formula_id=formula.formula_id,
            success=result.success,
            target_parameter=formula.target_parameter,
            value=result.value,
        )
        return result

    def evaluate_owner(self, owner_id: str) -> tuple[FormulaEvaluation, ...]:
        formulas = self.repository.for_owner(owner_id)
        by_target = {
            self.node_id(formula.owner_id, formula.target_parameter): formula
            for formula in formulas
        }
        order = self.graph.topological_order()
        results: list[FormulaEvaluation] = []
        for node in order:
            formula = by_target.get(node)
            if formula is not None:
                results.append(self.evaluate(formula.formula_id))
        return tuple(results)

    def propagate(self, owner_id: str, changed_parameter: str) -> tuple[FormulaEvaluation, ...]:
        source = self.node_id(owner_id, changed_parameter)
        affected = set(self.graph.transitive_dependents(source))
        formulas = {
            self.node_id(formula.owner_id, formula.target_parameter): formula
            for formula in self.repository.for_owner(owner_id)
        }
        results: list[FormulaEvaluation] = []
        for node in self.graph.topological_order():
            if node in affected and node in formulas:
                results.append(self.evaluate(formulas[node].formula_id))
        self._publish(
            "formula.propagation.completed",
            owner_id=owner_id,
            changed_parameter=changed_parameter,
            updated=len(results),
        )
        return tuple(results)

    def _publish(self, name: str, **payload) -> None:
        target = self.event_dispatcher
        if target is None:
            return
        if callable(target):
            target(name, payload)
            return
        dispatch = getattr(target, "dispatch", None)
        if callable(dispatch):
            try:
                dispatch(name, payload)
            except TypeError:
                dispatch({"name": name, "payload": payload})
