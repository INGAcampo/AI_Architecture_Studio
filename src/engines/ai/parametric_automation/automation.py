from __future__ import annotations
from dataclasses import dataclass
from typing import Any

from .formula import Formula
from .model import ParameterDefinition, ParameterSet
from .regeneration import RegenerationReport, RegenerationService
from .transaction import ParametricTransaction, TransactionResult


@dataclass(frozen=True, slots=True)
class AutomationResult:
    owner_id: str
    transaction: TransactionResult
    snapshot: dict[str, Any]

    @property
    def success(self) -> bool:
        return self.transaction.committed


class ParametricAutomationEngine:
    def __init__(self) -> None:
        self._parameter_sets: dict[str, ParameterSet] = {}
        self._regeneration_services: dict[str, RegenerationService] = {}

    def create_parameter_set(
        self,
        owner_id: str,
        definitions: tuple[ParameterDefinition, ...],
    ) -> ParameterSet:
        if owner_id in self._parameter_sets:
            raise ValueError(f"El owner ya existe: {owner_id}")

        parameter_set = ParameterSet(owner_id)
        for definition in definitions:
            parameter_set.define(definition)

        self._parameter_sets[owner_id] = parameter_set
        self._regeneration_services[owner_id] = RegenerationService()
        return parameter_set

    def register_formula(self, owner_id: str, formula: Formula) -> None:
        if formula.target_parameter_id not in self._parameter_sets[owner_id]:
            raise KeyError(formula.target_parameter_id)
        self._regeneration_services[owner_id].register_formula(formula)

    def set_values(
        self,
        owner_id: str,
        changes: dict[str, Any],
    ) -> AutomationResult:
        parameter_set = self._parameter_sets[owner_id]
        service = self._regeneration_services[owner_id]
        transaction = ParametricTransaction(parameter_set, service)

        for parameter_id, value in changes.items():
            transaction.set(parameter_id, value)

        result = transaction.commit()
        return AutomationResult(
            owner_id=owner_id,
            transaction=result,
            snapshot=parameter_set.snapshot(),
        )

    def regenerate(self, owner_id: str) -> RegenerationReport:
        return self._regeneration_services[owner_id].regenerate(
            self._parameter_sets[owner_id]
        )

    def parameters(self, owner_id: str) -> ParameterSet:
        return self._parameter_sets[owner_id]
