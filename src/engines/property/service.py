"""Fachada de aplicación para definiciones y valores de propiedades."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .definition import PropertyDefinition
from .exceptions import PropertyNotFoundError
from .registry import PropertyRegistry
from .units import UnitConverter
from .value import PropertyValue


class PropertyService:
    def __init__(
        self,
        registry: PropertyRegistry | None = None,
        unit_converter: UnitConverter | None = None,
    ) -> None:
        self.registry = registry or PropertyRegistry()
        self.units = unit_converter or UnitConverter()
        self._values: dict[str, dict[str, PropertyValue]] = {}

    def register_definition(
        self,
        definition: PropertyDefinition,
        *,
        replace: bool = False,
    ) -> PropertyDefinition:
        return self.registry.register(definition, replace=replace)

    def bind(
        self,
        owner_id: str,
        definition_name: str,
        value: Any = None,
        *,
        source: str = "instance",
        inherited: bool = False,
        calculated: bool = False,
    ) -> PropertyValue:
        definition = self.registry.require(definition_name)
        property_value = PropertyValue(
            definition=definition,
            value=value,
            source=source,
            inherited=inherited,
            calculated=calculated,
        )
        self._owner_values(owner_id)[self._key(definition.name)] = property_value
        return property_value

    def bind_many(
        self,
        owner_id: str,
        values: dict[str, Any],
    ) -> tuple[PropertyValue, ...]:
        return tuple(
            self.bind(owner_id, name, value)
            for name, value in values.items()
        )

    def get_value(
        self,
        owner_id: str,
        name: str,
        default: Any = None,
    ) -> Any:
        property_value = self.get_property(owner_id, name)
        return default if property_value is None else property_value.value

    def get_property(
        self,
        owner_id: str,
        name: str,
    ) -> PropertyValue | None:
        return self._values.get(str(owner_id), {}).get(self._key(name))

    def require_property(self, owner_id: str, name: str) -> PropertyValue:
        property_value = self.get_property(owner_id, name)
        if property_value is None:
            raise PropertyNotFoundError(
                f"{owner_id}:{name}"
            )
        return property_value

    def set_value(
        self,
        owner_id: str,
        name: str,
        value: Any,
        *,
        input_unit: str | None = None,
        force: bool = False,
    ) -> Any:
        property_value = self.require_property(owner_id, name)
        converted = value
        target_unit = property_value.definition.unit
        if (
            input_unit
            and target_unit
            and property_value.definition.property_type.is_numeric
        ):
            converted = self.units.convert(value, input_unit, target_unit)
        return property_value.set(converted, force=force)

    def remove_owner(self, owner_id: str) -> dict[str, PropertyValue]:
        return self._values.pop(str(owner_id), {})

    def properties_for(
        self,
        owner_id: str,
        *,
        visible_only: bool = False,
        group: str | None = None,
    ) -> tuple[PropertyValue, ...]:
        values: Iterable[PropertyValue] = self._values.get(
            str(owner_id), {}
        ).values()
        if visible_only:
            values = (
                item for item in values if item.definition.visible
            )
        if group is not None:
            normalized = str(group).strip().casefold()
            values = (
                item
                for item in values
                if str(
                    getattr(
                        item.definition.group,
                        "value",
                        item.definition.group,
                    )
                ).casefold()
                == normalized
            )
        return tuple(values)

    def snapshot(self, owner_id: str) -> dict[str, Any]:
        return {
            item.definition.name: item.value
            for item in self.properties_for(owner_id)
        }

    def _owner_values(self, owner_id: str) -> dict[str, PropertyValue]:
        return self._values.setdefault(str(owner_id), {})

    @staticmethod
    def _key(name: str) -> str:
        return str(name).strip().casefold()
