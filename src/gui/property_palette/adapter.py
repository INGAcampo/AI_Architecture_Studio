from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

from aias_i18n import tr

from .model import (
    PropertyDescriptor,
    PropertyEntry,
    PropertyValueType,
)


def _read(source: Any, property_id: str, default=None):
    if isinstance(source, dict):
        return source.get(property_id, default)

    properties = getattr(source, "properties", None)
    if isinstance(properties, dict) and property_id in properties:
        return properties[property_id]

    getter = getattr(source, "get_property", None)
    if callable(getter):
        try:
            return getter(property_id)
        except (KeyError, AttributeError):
            pass

    return getattr(source, property_id, default)


def _write(target: Any, property_id: str, value: Any) -> None:
    setter = getattr(target, "set_property", None)
    if callable(setter):
        setter(property_id, value)
        return

    properties = getattr(target, "properties", None)
    if isinstance(properties, dict):
        properties[property_id] = value
        return

    if isinstance(target, dict):
        target[property_id] = value
        return

    setattr(target, property_id, value)


class PropertySchemaRegistry:
    def __init__(self) -> None:
        self._schemas: dict[str, tuple[PropertyDescriptor, ...]] = {}

    def register(
        self,
        object_type: str,
        descriptors: Iterable[PropertyDescriptor],
        *,
        replace: bool = False,
    ) -> None:
        key = str(object_type)
        if key in self._schemas and not replace:
            raise KeyError(tr("property.schema_duplicate", schema_id=key))
        descriptors_tuple = tuple(descriptors)
        ids = [descriptor.property_id for descriptor in descriptors_tuple]
        if len(ids) != len(set(ids)):
            raise KeyError(tr("property.schema_duplicate_properties", schema_id=key))
        self._schemas[key] = descriptors_tuple

    def get(self, object_type: str) -> tuple[PropertyDescriptor, ...]:
        try:
            return self._schemas[str(object_type)]
        except KeyError as exc:
            raise KeyError(tr("property.schema_unknown", schema_id=object_type)) from exc

    def resolve(self, obj: Any) -> tuple[PropertyDescriptor, ...]:
        object_type = getattr(obj, "object_type", type(obj).__name__)
        if hasattr(object_type, "value"):
            object_type = object_type.value
        return self.get(str(object_type))


class PropertySelectionAdapter:
    def __init__(self, registry: PropertySchemaRegistry) -> None:
        self.registry = registry

    def build_entries(self, objects: Iterable[Any]) -> tuple[PropertyEntry, ...]:
        selected = tuple(objects)
        if not selected:
            return ()

        schemas = [self.registry.resolve(obj) for obj in selected]
        common_ids = set(descriptor.property_id for descriptor in schemas[0])
        for schema in schemas[1:]:
            common_ids.intersection_update(
                descriptor.property_id for descriptor in schema
            )

        first_schema = {
            descriptor.property_id: descriptor
            for descriptor in schemas[0]
        }
        entries: list[PropertyEntry] = []
        for property_id in (
            descriptor.property_id for descriptor in schemas[0]
            if descriptor.property_id in common_ids
        ):
            descriptor = first_schema[property_id]
            values = [_read(obj, property_id) for obj in selected]
            first = values[0]
            mixed = any(value != first for value in values[1:])
            entries.append(
                PropertyEntry(
                    descriptor=descriptor,
                    value=None if mixed else first,
                    mixed=mixed,
                )
            )
        return tuple(entries)

    def apply(self, objects: Iterable[Any], property_id: str, value: Any) -> None:
        for obj in objects:
            _write(obj, property_id, value)


def default_wall_schema() -> tuple[PropertyDescriptor, ...]:
    return (
        PropertyDescriptor(
            "name",
            tr("property.name"),
            group=tr("property.group.identity"),
            value_type=PropertyValueType.STRING,
        ),
        PropertyDescriptor(
            "ifc_class",
            tr("property.ifc_class"),
            group=tr("property.group.identity"),
            value_type=PropertyValueType.READ_ONLY,
            editable=False,
        ),
        PropertyDescriptor(
            "height",
            tr("property.height"),
            group=tr("property.group.dimensions"),
            value_type=PropertyValueType.LENGTH,
            unit="m",
            minimum=0.01,
        ),
        PropertyDescriptor(
            "thickness",
            tr("property.thickness"),
            group=tr("property.group.dimensions"),
            value_type=PropertyValueType.LENGTH,
            unit="m",
            minimum=0.001,
        ),
        PropertyDescriptor(
            "base_elevation",
            tr("property.base_elevation"),
            group=tr("property.group.constraints"),
            value_type=PropertyValueType.LENGTH,
            unit="m",
        ),
        PropertyDescriptor(
            "length",
            tr("property.length"),
            group=tr("property.group.quantities"),
            value_type=PropertyValueType.READ_ONLY,
            editable=False,
            unit="m",
        ),
        PropertyDescriptor(
            "area",
            tr("property.area"),
            group=tr("property.group.quantities"),
            value_type=PropertyValueType.READ_ONLY,
            editable=False,
            unit="m²",
        ),
        PropertyDescriptor(
            "volume",
            tr("property.volume"),
            group=tr("property.group.quantities"),
            value_type=PropertyValueType.READ_ONLY,
            editable=False,
            unit="m³",
        ),
    )
