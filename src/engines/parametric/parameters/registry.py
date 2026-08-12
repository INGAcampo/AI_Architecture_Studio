from __future__ import annotations

from typing import Iterable

from .types import ParameterDefinition, ParameterScope


class ParameterDefinitionRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, ParameterDefinition] = {}
        self.revision = 0

    def register(self, definition: ParameterDefinition, *, replace: bool = False) -> None:
        if definition.parameter_id in self._definitions and not replace:
            raise KeyError(f"Definición ya registrada: {definition.parameter_id}")
        self._definitions[definition.parameter_id] = definition
        self.revision += 1

    def register_many(self, definitions: Iterable[ParameterDefinition]) -> None:
        for definition in definitions:
            self.register(definition)

    def get(self, parameter_id: str) -> ParameterDefinition:
        try:
            return self._definitions[parameter_id]
        except KeyError as exc:
            raise KeyError(f"Definición desconocida: {parameter_id}") from exc

    def remove(self, parameter_id: str) -> ParameterDefinition:
        definition = self.get(parameter_id)
        self._definitions.pop(parameter_id)
        self.revision += 1
        return definition

    def all(self) -> tuple[ParameterDefinition, ...]:
        return tuple(self._definitions[key] for key in sorted(self._definitions))

    def by_group(self, group: str) -> tuple[ParameterDefinition, ...]:
        return tuple(definition for definition in self.all() if definition.group == group)

    def by_scope(self, scope: ParameterScope) -> tuple[ParameterDefinition, ...]:
        return tuple(definition for definition in self.all() if definition.scope is scope)
