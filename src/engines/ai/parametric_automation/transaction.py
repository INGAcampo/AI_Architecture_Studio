from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy
from typing import Any

from .model import ParameterSet
from .regeneration import RegenerationReport, RegenerationService


@dataclass(frozen=True, slots=True)
class TransactionResult:
    committed: bool
    changed_parameters: tuple[str, ...]
    regeneration_report: RegenerationReport | None
    error: str | None = None


class ParametricTransaction:
    def __init__(
        self,
        parameters: ParameterSet,
        regeneration_service: RegenerationService,
    ) -> None:
        self.parameters = parameters
        self.regeneration_service = regeneration_service
        self._changes: dict[str, Any] = {}

    def set(self, parameter_id: str, value: Any) -> None:
        self._changes[parameter_id] = value

    def commit(self) -> TransactionResult:
        snapshot = deepcopy(self.parameters)
        changed = []

        try:
            for parameter_id, value in self._changes.items():
                if self.parameters.set(parameter_id, value, source="transaction"):
                    changed.append(parameter_id)

            report = self.regeneration_service.regenerate(
                self.parameters,
                changed_parameter_ids=tuple(changed),
            )
            if not report.success:
                raise RuntimeError("; ".join(report.errors))
        except Exception as exc:
            self.parameters._values = snapshot._values
            self.parameters.revision = snapshot.revision
            return TransactionResult(
                committed=False,
                changed_parameters=(),
                regeneration_report=None,
                error=str(exc),
            )

        return TransactionResult(
            committed=True,
            changed_parameters=tuple(changed),
            regeneration_report=report,
        )
