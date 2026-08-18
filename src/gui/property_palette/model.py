from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Iterable
from aias_i18n import tr


class PropertyValueType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    ENUM = "enum"
    LENGTH = "length"
    AREA = "area"
    VOLUME = "volume"
    READ_ONLY = "read_only"


Validator = Callable[[Any], bool | None]


@dataclass(frozen=True, slots=True)
class PropertyDescriptor:
    property_id: str
    label: str
    group: str = field(default_factory=lambda: tr("property.group.general"))
    value_type: PropertyValueType = PropertyValueType.STRING
    editable: bool = True
    unit: str | None = None
    enum_values: tuple[str, ...] = ()
    minimum: float | None = None
    maximum: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    validator: Validator | None = field(default=None, compare=False, repr=False)

    def __post_init__(self) -> None:
        if not self.property_id.strip():
            raise ValueError(tr("error.empty_property_id"))
        if not self.label.strip():
            raise ValueError(tr("error.empty_property_label"))
        if self.value_type is PropertyValueType.ENUM and not self.enum_values:
            raise ValueError(tr("error.enum_values_required"))
        if (
            self.minimum is not None
            and self.maximum is not None
            and self.minimum > self.maximum
        ):
            raise ValueError(tr("error.minimum_above_maximum"))


@dataclass(slots=True)
class PropertyEntry:
    descriptor: PropertyDescriptor
    value: Any = None
    mixed: bool = False
    error: str | None = None

    def display_value(self) -> str:
        if self.mixed:
            return tr("property.mixed")
        if self.value is None:
            return ""
        if self.descriptor.value_type is PropertyValueType.BOOLEAN:
            return tr("common.yes") if bool(self.value) else tr("common.no")
        suffix = f" {self.descriptor.unit}" if self.descriptor.unit else ""
        return f"{self.value}{suffix}"


class PropertyPaletteModel:
    def __init__(self) -> None:
        self._entries: dict[str, PropertyEntry] = {}
        self._group_order: list[str] = []
        self.revision = 0

    def _touch(self) -> int:
        self.revision += 1
        return self.revision

    def set_entries(self, entries: Iterable[PropertyEntry]) -> None:
        mapped: dict[str, PropertyEntry] = {}
        groups: list[str] = []
        for entry in entries:
            key = entry.descriptor.property_id
            if key in mapped:
                raise KeyError(tr("error.duplicate_property",property_id=key))
            mapped[key] = entry
            if entry.descriptor.group not in groups:
                groups.append(entry.descriptor.group)
        self._entries = mapped
        self._group_order = groups
        self._touch()

    def clear(self) -> None:
        if self._entries:
            self._entries.clear()
            self._group_order.clear()
            self._touch()

    def require(self, property_id: str) -> PropertyEntry:
        try:
            return self._entries[property_id]
        except KeyError as exc:
            raise KeyError(tr("error.unknown_property",property_id=property_id)) from exc

    def entries(self) -> tuple[PropertyEntry, ...]:
        return tuple(self._entries.values())

    def groups(self) -> tuple[str, ...]:
        return tuple(self._group_order)

    def entries_in_group(self, group: str) -> tuple[PropertyEntry, ...]:
        return tuple(
            entry for entry in self._entries.values()
            if entry.descriptor.group == group
        )

    def filter(self, query: str) -> tuple[PropertyEntry, ...]:
        text = query.strip().casefold()
        if not text:
            return self.entries()
        return tuple(
            entry for entry in self._entries.values()
            if text in entry.descriptor.label.casefold()
            or text in entry.descriptor.property_id.casefold()
            or text in entry.descriptor.group.casefold()
        )

    def update_value(self, property_id: str, value: Any) -> PropertyEntry:
        entry = self.require(property_id)
        descriptor = entry.descriptor
        if not descriptor.editable or descriptor.value_type is PropertyValueType.READ_ONLY:
            raise PermissionError(tr("error.read_only_property",property_id=property_id))

        normalized = self._normalize(descriptor, value)
        self._validate(descriptor, normalized)

        changed = entry.mixed or entry.value != normalized or entry.error is not None
        entry.value = normalized
        entry.mixed = False
        entry.error = None
        if changed:
            self._touch()
        return entry

    def _normalize(self, descriptor: PropertyDescriptor, value: Any) -> Any:
        kind = descriptor.value_type
        if kind in {
            PropertyValueType.STRING,
            PropertyValueType.ENUM,
            PropertyValueType.READ_ONLY,
        }:
            return "" if value is None else str(value)
        if kind is PropertyValueType.BOOLEAN:
            if isinstance(value, str):
                normalized = value.strip().casefold()
                if normalized in {"true", "1", "yes", "sí", "si"}:
                    return True
                if normalized in {"false", "0", "no"}:
                    return False
                raise ValueError(tr("error.invalid_boolean",value=value))
            return bool(value)
        if kind is PropertyValueType.INTEGER:
            if isinstance(value, bool):
                raise ValueError(tr("error.boolean_not_integer"))
            return int(value)
        if kind in {
            PropertyValueType.FLOAT,
            PropertyValueType.LENGTH,
            PropertyValueType.AREA,
            PropertyValueType.VOLUME,
        }:
            if isinstance(value, bool):
                raise ValueError(tr("error.boolean_not_number"))
            return float(value)
        return value

    def _validate(self, descriptor: PropertyDescriptor, value: Any) -> None:
        if descriptor.enum_values and str(value) not in descriptor.enum_values:
            raise ValueError(tr("error.value_not_allowed",property_id=descriptor.property_id,value=value))

        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if descriptor.minimum is not None and value < descriptor.minimum:
                raise ValueError(tr("error.minimum",property_id=descriptor.property_id,minimum=descriptor.minimum))
            if descriptor.maximum is not None and value > descriptor.maximum:
                raise ValueError(tr("error.maximum",property_id=descriptor.property_id,maximum=descriptor.maximum))

        if descriptor.validator is not None:
            accepted = descriptor.validator(value)
            if accepted is False:
                raise ValueError(tr("error.custom_validation",property_id=descriptor.property_id))
