"""Elemento BIM neutral que puede envolver objetos existentes de AIAS."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from .categories import BimCategory
from .parameters import BimParameterSet


@dataclass
class BimElement:
    name: str
    category: BimCategory | str
    element_id: str = field(default_factory=lambda: str(uuid4()))
    type_name: str = ""
    level_id: str | None = None
    geometry_ref: Any = None
    source_object_id: str | None = None
    parameters: BimParameterSet = field(default_factory=BimParameterSet)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.name = str(self.name).strip() or "Elemento BIM"
        self.category = BimCategory.coerce(self.category)
        self.element_id = str(self.element_id)
        self.type_name = str(self.type_name or self.category.value)
        self.metadata = dict(self.metadata or {})

        if not isinstance(self.parameters, BimParameterSet):
            self.parameters = BimParameterSet(self.parameters)

    @classmethod
    def from_aias_object(
        cls,
        source: Any,
        *,
        category: BimCategory | str | None = None,
        level_id: str | None = None,
    ) -> "BimElement":
        detected = category or getattr(source, "object_type", "Generic")
        try:
            bim_category = BimCategory.coerce(detected)
        except ValueError:
            bim_category = BimCategory.GENERIC

        parameters = BimParameterSet(
            deepcopy(getattr(source, "properties", {}) or {})
        )

        return cls(
            name=getattr(source, "name", source.__class__.__name__),
            category=bim_category,
            element_id=str(getattr(source, "id", uuid4())),
            type_name=source.__class__.__name__,
            level_id=level_id,
            geometry_ref=getattr(source, "geometry", None),
            source_object_id=str(getattr(source, "id", "")) or None,
            parameters=parameters,
            metadata={
                "aias_module": source.__class__.__module__,
                "aias_class": source.__class__.__name__,
            },
        )

    def set_parameter(
        self,
        name: str,
        value: Any,
        *,
        unit: str | None = None,
        group: str = "General",
    ) -> None:
        self.parameters.set(name, value, unit=unit, group=group)

    def to_dict(self) -> dict[str, Any]:
        return {
            "element_id": self.element_id,
            "name": self.name,
            "category": self.category.value,
            "type_name": self.type_name,
            "level_id": self.level_id,
            "source_object_id": self.source_object_id,
            "parameters": self.parameters.to_dict(),
            "metadata": deepcopy(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BimElement":
        return cls(
            element_id=data["element_id"],
            name=data["name"],
            category=data["category"],
            type_name=data.get("type_name", ""),
            level_id=data.get("level_id"),
            source_object_id=data.get("source_object_id"),
            parameters=BimParameterSet.from_dict(
                data.get("parameters", {})
            ),
            metadata=data.get("metadata", {}),
        )
