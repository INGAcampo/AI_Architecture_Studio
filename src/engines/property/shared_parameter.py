"""Definiciones reutilizables de parámetros compartidos."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any
from uuid import uuid4

from .definition import PropertyDefinition


class ParameterDiscipline(str, Enum):
    COMMON = "common"
    ARCHITECTURE = "architecture"
    STRUCTURAL = "structural"
    MEP = "mep"
    TOPOGRAPHY = "topography"
    COST = "cost"
    ENERGY = "energy"
    FACILITY = "facility"
    CUSTOM = "custom"


class ParameterScope(str, Enum):
    PROJECT = "project"
    CATEGORY = "category"
    FAMILY = "family"
    TYPE = "type"
    INSTANCE = "instance"
    SELECTION = "selection"


@dataclass(frozen=True)
class IfcMapping:
    property_set: str
    property_name: str

    def to_dict(self) -> dict[str, str]:
        return {
            "property_set": self.property_set,
            "property_name": self.property_name,
        }


@dataclass(frozen=True)
class SharedParameter:
    definition: PropertyDefinition
    discipline: ParameterDiscipline | str = ParameterDiscipline.COMMON
    scope: ParameterScope | str = ParameterScope.INSTANCE
    guid: str = field(default_factory=lambda: str(uuid4()))
    version: int = 1
    tags: tuple[str, ...] = field(default_factory=tuple)
    ifc_mapping: IfcMapping | None = None
    deprecated: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "discipline",
            ParameterDiscipline(self.discipline),
        )
        object.__setattr__(self, "scope", ParameterScope(self.scope))
        object.__setattr__(
            self,
            "tags",
            tuple(
                sorted(
                    {
                        str(tag).strip()
                        for tag in self.tags
                        if str(tag).strip()
                    }
                )
            ),
        )
        if self.version < 1:
            raise ValueError("La versión debe ser mayor o igual que 1.")

    @property
    def name(self) -> str:
        return self.definition.name

    def to_dict(self) -> dict[str, Any]:
        return {
            "guid": self.guid,
            "version": self.version,
            "discipline": self.discipline.value,
            "scope": self.scope.value,
            "tags": list(self.tags),
            "deprecated": self.deprecated,
            "definition": self.definition.to_dict(),
            "ifc_mapping": (
                self.ifc_mapping.to_dict()
                if self.ifc_mapping is not None
                else None
            ),
        }
