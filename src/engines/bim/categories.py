"""Categorías BIM neutrales y extensibles."""

from __future__ import annotations

from enum import Enum


class BimCategory(str, Enum):
    PROJECT = "Project"
    SITE = "Site"
    BUILDING = "Building"
    STOREY = "Storey"
    GRID = "Grid"
    SPACE = "Space"
    WALL = "Wall"
    SLAB = "Slab"
    ROOF = "Roof"
    DOOR = "Door"
    WINDOW = "Window"
    COLUMN = "Column"
    BEAM = "Beam"
    FOUNDATION = "Foundation"
    STAIR = "Stair"
    RAILING = "Railing"
    FURNITURE = "Furniture"
    EQUIPMENT = "Equipment"
    GENERIC = "Generic"

    @classmethod
    def coerce(cls, value: "BimCategory | str") -> "BimCategory":
        if isinstance(value, cls):
            return value

        normalized = str(value).strip().lower()
        for category in cls:
            if normalized in {
                category.name.lower(),
                category.value.lower(),
            }:
                return category

        raise ValueError(f"Categoría BIM no reconocida: {value!r}")
