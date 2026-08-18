"""Biblioteca de parámetros compartidos y sus bindings."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any
import json

from .definition import PropertyDefinition
from .exceptions import (
    DuplicatePropertyError,
    PropertyNotFoundError,
)
from .groups import PropertyGroup
from .parameter_binding import ParameterBinding
from .service import PropertyService
from .shared_parameter import (
    IfcMapping,
    ParameterDiscipline,
    ParameterScope,
    SharedParameter,
)
from .types import PropertyType


class SharedParameterLibrary:
    SCHEMA_VERSION = "1.0"

    def __init__(self, name: str = "AIAS Shared Parameters") -> None:
        self.name = str(name).strip() or "AIAS Shared Parameters"
        self._parameters_by_guid: dict[str, SharedParameter] = {}
        self._guid_by_name: dict[str, str] = {}
        self._bindings: list[ParameterBinding] = []

    def __len__(self) -> int:
        return len(self._parameters_by_guid)

    def __iter__(self) -> Iterator[SharedParameter]:
        return iter(self._parameters_by_guid.values())

    @property
    def bindings(self) -> tuple[ParameterBinding, ...]:
        return tuple(self._bindings)

    def register(
        self,
        parameter: SharedParameter,
        *,
        replace: bool = False,
    ) -> SharedParameter:
        name_key = self._key(parameter.name)
        existing_guid = self._guid_by_name.get(name_key)

        if (
            not replace
            and (
                parameter.guid in self._parameters_by_guid
                or existing_guid is not None
            )
        ):
            raise DuplicatePropertyError(
                f"Ya existe el parámetro compartido {parameter.name!r}."
            )

        if replace and existing_guid is not None:
            self._parameters_by_guid.pop(existing_guid, None)

        self._parameters_by_guid[parameter.guid] = parameter
        self._guid_by_name[name_key] = parameter.guid
        return parameter

    def get(self, identifier: str) -> SharedParameter | None:
        if identifier in self._parameters_by_guid:
            return self._parameters_by_guid[identifier]
        guid = self._guid_by_name.get(self._key(identifier))
        return self._parameters_by_guid.get(guid) if guid else None

    def require(self, identifier: str) -> SharedParameter:
        parameter = self.get(identifier)
        if parameter is None:
            raise PropertyNotFoundError(identifier)
        return parameter

    def add_binding(self, binding: ParameterBinding) -> ParameterBinding:
        self.require(binding.parameter_guid)
        if binding not in self._bindings:
            self._bindings.append(binding)
        return binding

    def parameters_for(
        self,
        *,
        owner_id: str | None = None,
        category: str | None = None,
        family: str | None = None,
        discipline: ParameterDiscipline | str | None = None,
        include_deprecated: bool = False,
    ) -> tuple[SharedParameter, ...]:
        normalized_discipline = (
            ParameterDiscipline(discipline)
            if discipline is not None
            else None
        )
        matching: list[SharedParameter] = []

        for parameter in self:
            if parameter.deprecated and not include_deprecated:
                continue
            if (
                normalized_discipline is not None
                and parameter.discipline is not normalized_discipline
            ):
                continue

            bindings = [
                binding
                for binding in self._bindings
                if binding.parameter_guid == parameter.guid
            ]
            if not bindings or any(
                binding.applies_to(
                    owner_id=owner_id,
                    category=category,
                    family=family,
                )
                for binding in bindings
            ):
                matching.append(parameter)

        return tuple(matching)

    def install_into(
        self,
        service: PropertyService,
        *,
        replace: bool = False,
    ) -> tuple[PropertyDefinition, ...]:
        installed = []
        for parameter in self:
            service.register_definition(
                parameter.definition,
                replace=replace,
            )
            installed.append(parameter.definition)
        return tuple(installed)

    def bind_owner(
        self,
        service: PropertyService,
        owner_id: str,
        *,
        category: str | None = None,
        family: str | None = None,
        values: dict[str, Any] | None = None,
    ):
        values = values or {}
        bound = []
        for parameter in self.parameters_for(
            owner_id=owner_id,
            category=category,
            family=family,
        ):
            current = service.registry.get(parameter.name)
            if current is None:
                service.register_definition(parameter.definition)
            initial = values.get(parameter.name, parameter.definition.default)
            bound.append(
                service.bind(
                    owner_id,
                    parameter.name,
                    initial,
                    source="shared",
                )
            )
        return tuple(bound)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.SCHEMA_VERSION,
            "name": self.name,
            "parameters": [parameter.to_dict() for parameter in self],
            "bindings": [binding.to_dict() for binding in self._bindings],
        }

    def save(self, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(
            json.dumps(
                self.to_dict(),
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        temporary.replace(target)
        return target

    @classmethod
    def load(cls, path: str | Path) -> "SharedParameterLibrary":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SharedParameterLibrary":
        library = cls(data.get("name", "AIAS Shared Parameters"))
        for raw in data.get("parameters", []):
            definition_raw = raw["definition"]
            definition = PropertyDefinition(
                definition_id=definition_raw.get("definition_id") or raw["guid"],
                name=definition_raw["name"],
                display_name=definition_raw.get("display_name"),
                property_type=PropertyType(definition_raw["property_type"]),
                group=PropertyGroup.coerce(
                    definition_raw.get("group", "General")
                ),
                unit=definition_raw.get("unit"),
                default=definition_raw.get("default"),
                required=bool(definition_raw.get("required", False)),
                read_only=bool(definition_raw.get("read_only", False)),
                visible=bool(definition_raw.get("visible", True)),
                description=definition_raw.get("description", ""),
            )
            mapping_raw = raw.get("ifc_mapping")
            mapping = (
                IfcMapping(
                    mapping_raw["property_set"],
                    mapping_raw["property_name"],
                )
                if mapping_raw
                else None
            )
            library.register(
                SharedParameter(
                    guid=raw["guid"],
                    version=int(raw.get("version", 1)),
                    discipline=raw.get("discipline", "common"),
                    scope=raw.get("scope", "instance"),
                    tags=tuple(raw.get("tags", ())),
                    deprecated=bool(raw.get("deprecated", False)),
                    definition=definition,
                    ifc_mapping=mapping,
                )
            )

        for raw in data.get("bindings", []):
            library.add_binding(
                ParameterBinding(
                    parameter_guid=raw["parameter_guid"],
                    scope=ParameterScope(raw.get("scope", "instance")),
                    categories=tuple(raw.get("categories", ())),
                    families=tuple(raw.get("families", ())),
                    target_ids=tuple(raw.get("target_ids", ())),
                    required=bool(raw.get("required", False)),
                )
            )
        return library

    @staticmethod
    def _key(value: str) -> str:
        return str(value).strip().casefold()
