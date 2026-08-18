"""Registro central de definiciones de propiedades."""

from __future__ import annotations

from collections.abc import Iterator

from .definition import PropertyDefinition
from .exceptions import DuplicatePropertyError, PropertyNotFoundError


class PropertyRegistry:
    def __init__(self) -> None:
        self._definitions: dict[str, PropertyDefinition] = {}

    def __len__(self) -> int:
        return len(self._definitions)

    def __iter__(self) -> Iterator[PropertyDefinition]:
        return iter(self._definitions.values())

    def register(
        self,
        definition: PropertyDefinition,
        *,
        replace: bool = False,
    ) -> PropertyDefinition:
        key = self._key(definition.name)
        if key in self._definitions and not replace:
            raise DuplicatePropertyError(
                f"Ya existe la propiedad {definition.name!r}."
            )
        self._definitions[key] = definition
        return definition

    def get(self, name: str) -> PropertyDefinition | None:
        return self._definitions.get(self._key(name))

    def require(self, name: str) -> PropertyDefinition:
        definition = self.get(name)
        if definition is None:
            raise PropertyNotFoundError(name)
        return definition

    def remove(self, name: str) -> PropertyDefinition:
        key = self._key(name)
        try:
            return self._definitions.pop(key)
        except KeyError as error:
            raise PropertyNotFoundError(name) from error

    def definitions_for_group(self, group: str) -> tuple[PropertyDefinition, ...]:
        normalized = str(group).strip().casefold()
        return tuple(
            definition
            for definition in self._definitions.values()
            if str(getattr(definition.group, "value", definition.group))
            .casefold()
            == normalized
        )

    @staticmethod
    def _key(name: str) -> str:
        return str(name).strip().casefold()
