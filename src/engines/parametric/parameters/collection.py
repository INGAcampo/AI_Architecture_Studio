from __future__ import annotations

from typing import Any, Iterable

from .types import ParameterAccess, ParameterDefinition, ParameterValue
from .validator import ParameterValidator


class ParameterCollection:
    def __init__(
        self,
        owner_id: str,
        *,
        validator: ParameterValidator | None = None,
    ) -> None:
        if not owner_id.strip():
            raise ValueError("owner_id no puede estar vacío")
        self.owner_id = owner_id
        self.validator = validator or ParameterValidator()
        self._values: dict[str, ParameterValue] = {}
        self.revision = 0

    def add_definition(
        self,
        definition: ParameterDefinition,
        *,
        initial_value: Any = None,
        source: str = "default",
    ) -> ParameterValue:
        if definition.parameter_id in self._values:
            raise KeyError(f"Parámetro ya existente: {definition.parameter_id}")
        raw = definition.default_value if initial_value is None else initial_value
        normalized = self.validator.normalize(definition, raw)
        value = ParameterValue(definition, normalized, revision=0, source=source)
        self._values[definition.parameter_id] = value
        self.revision += 1
        return value

    def add_definitions(self, definitions: Iterable[ParameterDefinition]) -> None:
        for definition in definitions:
            self.add_definition(definition)

    def get(self, parameter_id: str) -> ParameterValue:
        try:
            return self._values[parameter_id]
        except KeyError as exc:
            raise KeyError(f"Parámetro desconocido: {parameter_id}") from exc

    def value(self, parameter_id: str) -> Any:
        return self.get(parameter_id).value

    def set(
        self,
        parameter_id: str,
        value: Any,
        *,
        source: str = "user",
        allow_read_only: bool = False,
    ) -> ParameterValue:
        current = self.get(parameter_id)
        if (
            current.definition.access is not ParameterAccess.READ_WRITE
            and not allow_read_only
        ):
            raise PermissionError(f"Parámetro no editable: {parameter_id}")
        normalized = self.validator.normalize(current.definition, value)
        if current.value != normalized:
            current.value = normalized
            current.revision += 1
            current.source = source
            current.error = None
            self.revision += 1
        return current

    def set_calculated(self, parameter_id: str, value: Any, *, source: str = "formula") -> ParameterValue:
        return self.set(parameter_id, value, source=source, allow_read_only=True)

    def remove(self, parameter_id: str) -> ParameterValue:
        value = self.get(parameter_id)
        self._values.pop(parameter_id)
        self.revision += 1
        return value

    def all(self) -> tuple[ParameterValue, ...]:
        return tuple(self._values[key] for key in sorted(self._values))

    def snapshot(self) -> dict[str, Any]:
        return {
            "owner_id": self.owner_id,
            "revision": self.revision,
            "values": {
                key: value.snapshot()
                for key, value in sorted(self._values.items())
            },
        }
