"""Grupos estándar utilizados por el Inspector BIM y otros clientes."""

from enum import Enum


class PropertyGroup(str, Enum):
    IDENTITY = "Identity"
    GEOMETRY = "Geometry"
    CONSTRAINTS = "Constraints"
    MATERIALS = "Materials"
    STRUCTURAL = "Structural"
    ANALYSIS = "Analysis"
    LOADS = "Loads"
    MEP = "MEP"
    ENERGY = "Energy"
    COST = "Cost"
    CLASSIFICATION = "Classification"
    PHASING = "Phasing"
    CUSTOM = "Custom"
    GENERAL = "General"

    @classmethod
    def coerce(cls, value: "PropertyGroup | str") -> "PropertyGroup | str":
        if isinstance(value, cls):
            return value
        normalized = str(value).strip()
        for group in cls:
            if normalized.lower() in {group.name.lower(), group.value.lower()}:
                return group
        return normalized or cls.GENERAL
