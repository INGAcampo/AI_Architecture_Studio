"""Adaptadores BIM para objetos arquitectónicos y estructurales de AIAS."""

from __future__ import annotations

from typing import Any

from models.architectural.door import Door
from models.architectural.grid import Grid
from models.architectural.level import Level
from models.architectural.room import Room
from models.architectural.slab import Slab
from models.architectural.wall import Wall
from models.architectural.window import Window
from models.structural.beam import Beam
from models.structural.column import Column
from models.structural.foundation import Foundation

from ..categories import BimCategory
from ..element import BimElement
from ..parameters import BimParameterSet
from .base import BimAdapter


class LevelBimAdapter(BimAdapter):
    category = BimCategory.STOREY
    source_types = (Level,)

    def to_bim_element(self, source: Level, *, level_id=None) -> BimElement:
        parameters = BimParameterSet()
        self.add_parameter(
            parameters, "Elevation", source.elevation,
            unit="m", group="Constraints",
        )
        self.add_parameter(
            parameters, "Visible", source.visible, group="Identity",
        )
        self.add_parameter(
            parameters, "Active", source.active, group="Identity",
        )
        return self.build_element(
            source,
            level_id=level_id,
            parameters=parameters,
            metadata={"native_role": "level"},
        )


class GridBimAdapter(BimAdapter):
    category = BimCategory.GRID
    source_types = (Grid,)

    def to_bim_element(self, source: Grid, *, level_id=None) -> BimElement:
        parameters = BimParameterSet()
        self.add_parameter(parameters, "Label", source.label, group="Identity")
        self.add_parameter(
            parameters, "Visible", source.visible, group="Identity",
        )
        return self.build_element(
            source,
            level_id=level_id,
            parameters=parameters,
            metadata={
                "native_role": "grid",
                "start": _point_data(source.start),
                "end": _point_data(source.end),
            },
        )


class WallBimAdapter(BimAdapter):
    category = BimCategory.WALL
    source_types = (Wall,)

    def to_bim_element(self, source: Wall, *, level_id=None) -> BimElement:
        parameters = self.source_properties(source)
        values = (
            ("Thickness", source.thickness, "m", "Geometry"),
            ("Height", source.height, "m", "Geometry"),
            ("Length", source.length, "m", "Quantities"),
            ("PlanArea", source.area_2d, "m²", "Quantities"),
            ("Justification", source.justification, None, "Constraints"),
            ("BaseLevel", source.base_level, None, "Constraints"),
            ("OpeningCount", source.opening_count, None, "Identity"),
        )
        for name, value, unit, group in values:
            self.add_parameter(
                parameters, name, value, unit=unit, group=group,
            )
        return self.build_element(
            source,
            level_id=level_id,
            parameters=parameters,
            metadata={"native_role": "host"},
        )


class DoorBimAdapter(BimAdapter):
    category = BimCategory.DOOR
    source_types = (Door,)

    def to_bim_element(self, source: Door, *, level_id=None) -> BimElement:
        parameters = BimParameterSet()
        values = (
            ("Width", source.width, "m", "Geometry"),
            ("Height", source.height, "m", "Geometry"),
            ("Handedness", source.handedness, None, "Operation"),
            ("SwingDirection", source.swing_direction, None, "Operation"),
            ("DoorType", source.door_type, None, "Identity"),
        )
        for name, value, unit, group in values:
            self.add_parameter(
                parameters, name, value, unit=unit, group=group,
            )
        return self.build_element(
            source,
            level_id=level_id,
            parameters=parameters,
            metadata={"native_role": "opening_fill"},
        )


class WindowBimAdapter(BimAdapter):
    category = BimCategory.WINDOW
    source_types = (Window,)

    def to_bim_element(self, source: Window, *, level_id=None) -> BimElement:
        parameters = BimParameterSet()
        values = (
            ("Width", source.width, "m", "Geometry"),
            ("Height", source.height, "m", "Geometry"),
            ("SillHeight", source.sill_height, "m", "Constraints"),
            ("WindowType", source.window_type, None, "Identity"),
        )
        for name, value, unit, group in values:
            self.add_parameter(
                parameters, name, value, unit=unit, group=group,
            )
        return self.build_element(
            source,
            level_id=level_id,
            parameters=parameters,
            metadata={"native_role": "opening_fill"},
        )


class RoomBimAdapter(BimAdapter):
    category = BimCategory.SPACE
    source_types = (Room,)

    def to_bim_element(self, source: Room, *, level_id=None) -> BimElement:
        parameters = self.source_properties(source)
        values = (
            ("Number", source.number, None, "Identity"),
            ("Category", source.category, None, "Identity"),
            ("CategoryLabel", source.category_label, None, "Identity"),
            ("Area", source.area, "m²", "Quantities"),
            ("Perimeter", source.perimeter, "m", "Quantities"),
            ("Comments", source.comments, None, "Identity"),
            ("Valid", source.valid, None, "Validation"),
        )
        for name, value, unit, group in values:
            self.add_parameter(
                parameters, name, value, unit=unit, group=group,
            )
        return self.build_element(
            source,
            level_id=level_id,
            parameters=parameters,
            metadata={"native_role": "space"},
        )


class SlabBimAdapter(BimAdapter):
    category = BimCategory.SLAB
    source_types = (Slab,)

    def to_bim_element(self, source: Slab, *, level_id=None) -> BimElement:
        parameters = self.source_properties(source)
        values = (
            ("Thickness", source.thickness, "m", "Geometry"),
            ("Elevation", source.elevation, "m", "Constraints"),
            ("Material", source.material, None, "Materials"),
            ("Area", source.area, "m²", "Quantities"),
            ("Perimeter", source.perimeter, "m", "Quantities"),
            ("Volume", source.volume, "m³", "Quantities"),
            ("ConcreteStrength", source.concrete_strength_mpa, "MPa", "Structural"),
            ("Density", source.density_kg_m3, "kg/m³", "Structural"),
            ("LiveLoad", source.live_load_kg_m2, "kg/m²", "Loads"),
            ("TotalServiceLoad", source.total_service_load_kg_m2, "kg/m²", "Loads"),
        )
        for name, value, unit, group in values:
            self.add_parameter(
                parameters, name, value, unit=unit, group=group,
            )
        return self.build_element(
            source,
            level_id=level_id,
            parameters=parameters,
            metadata={
                "native_role": "horizontal_element",
                "host_room_id": source.host_room_id,
            },
        )


class BeamBimAdapter(BimAdapter):
    category = BimCategory.BEAM
    source_types = (Beam,)

    def to_bim_element(self, source: Beam, *, level_id=None) -> BimElement:
        parameters = self.source_properties(source)
        for name, value, unit, group in (
            ("Level", source.level, None, "Constraints"),
            ("BeamType", source.beam_type, None, "Identity"),
            ("Material", source.material, None, "Materials"),
            ("ConcreteStrength", source.concrete_strength_mpa, "MPa", "Structural"),
            ("SteelGrade", source.steel_grade, None, "Structural"),
            ("Profile", source.profile, None, "Geometry"),
            ("Cover", source.cover_cm, "cm", "Structural"),
            ("DesignCode", source.design_code, None, "Structural"),
            ("Length", source.length, "m", "Quantities"),
            ("Volume", source.volume, "m³", "Quantities"),
        ):
            self.add_parameter(
                parameters, name, value, unit=unit, group=group,
            )
        return self.build_element(
            source,
            level_id=level_id,
            parameters=parameters,
            metadata={"native_role": "structural_frame"},
        )


class ColumnBimAdapter(BimAdapter):
    category = BimCategory.COLUMN
    source_types = (Column,)

    def to_bim_element(self, source: Column, *, level_id=None) -> BimElement:
        parameters = self.source_properties(source)
        for name, value, unit, group in (
            ("Level", source.level, None, "Constraints"),
            ("Material", source.material, None, "Materials"),
            ("ConcreteStrength", source.concrete_strength_mpa, "MPa", "Structural"),
            ("SteelGrade", source.steel_grade, None, "Structural"),
            ("Width", source.width, "m", "Geometry"),
            ("Depth", source.depth, "m", "Geometry"),
            ("Height", source.height, "m", "Geometry"),
            ("Cover", source.cover_cm, "cm", "Structural"),
            ("DesignCode", source.design_code, None, "Structural"),
            ("Volume", source.volume, "m³", "Quantities"),
        ):
            self.add_parameter(
                parameters, name, value, unit=unit, group=group,
            )
        return self.build_element(
            source,
            level_id=level_id,
            parameters=parameters,
            metadata={"native_role": "structural_column"},
        )


class FoundationBimAdapter(BimAdapter):
    category = BimCategory.FOUNDATION
    source_types = (Foundation,)

    def to_bim_element(
        self,
        source: Foundation,
        *,
        level_id=None,
    ) -> BimElement:
        parameters = self.source_properties(source)
        for name, value, unit, group in (
            ("Level", source.level, None, "Constraints"),
            ("FoundationType", source.foundation_type, None, "Identity"),
            ("Material", source.material, None, "Materials"),
            ("ConcreteStrength", source.concrete_strength_mpa, "MPa", "Structural"),
            ("SoilBearingCapacity", source.soil_bearing_capacity_kpa, "kPa", "Geotechnical"),
            ("FoundationDepth", source.foundation_depth_m, "m", "Geotechnical"),
            ("DesignCode", source.design_code, None, "Structural"),
            ("Volume", source.volume, "m³", "Quantities"),
        ):
            self.add_parameter(
                parameters, name, value, unit=unit, group=group,
            )
        return self.build_element(
            source,
            level_id=level_id,
            parameters=parameters,
            metadata={"native_role": "structural_foundation"},
        )


def _point_data(point: Any) -> dict[str, float] | None:
    if point is None:
        return None
    return {
        "x": float(getattr(point, "x", 0.0)),
        "y": float(getattr(point, "y", 0.0)),
        "z": float(getattr(point, "z", 0.0)),
    }
