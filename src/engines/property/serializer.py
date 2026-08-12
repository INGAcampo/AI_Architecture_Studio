"""Serialización JSON-compatible del Property Engine."""

from __future__ import annotations

from typing import Any

from .definition import PropertyDefinition
from .groups import PropertyGroup
from .registry import PropertyRegistry
from .service import PropertyService
from .types import PropertyType


class PropertySerializer:
    @staticmethod
    def definitions_to_dict(
        registry: PropertyRegistry,
    ) -> list[dict[str, Any]]:
        return [definition.to_dict() for definition in registry]

    @staticmethod
    def definition_from_dict(
        data: dict[str, Any],
    ) -> PropertyDefinition:
        return PropertyDefinition(
            definition_id=data.get("definition_id", ""),
            name=data["name"],
            display_name=data.get("display_name"),
            property_type=PropertyType(data["property_type"]),
            group=PropertyGroup.coerce(data.get("group", "General")),
            unit=data.get("unit"),
            default=data.get("default"),
            required=bool(data.get("required", False)),
            read_only=bool(data.get("read_only", False)),
            visible=bool(data.get("visible", True)),
            description=data.get("description", ""),
        )

    @classmethod
    def registry_from_dict(
        cls,
        data: list[dict[str, Any]],
    ) -> PropertyRegistry:
        registry = PropertyRegistry()
        for raw in data:
            registry.register(cls.definition_from_dict(raw))
        return registry

    @staticmethod
    def owner_values_to_dict(
        service: PropertyService,
        owner_id: str,
    ) -> dict[str, Any]:
        return {
            "owner_id": str(owner_id),
            "values": [
                item.to_dict()
                for item in service.properties_for(owner_id)
            ],
        }
