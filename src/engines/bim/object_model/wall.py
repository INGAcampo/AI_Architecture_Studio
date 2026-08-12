from __future__ import annotations

from dataclasses import dataclass
import math
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from engines.bim.object_model.core import (
    BimObject,
    MaterialRef,
    ObjectId,
    ObjectType,
)


_EPSILON = 1e-9


@dataclass(frozen=True)
class WallPoint:
    x: float
    y: float
    z: float = 0.0

    def __post_init__(self) -> None:
        for value in (self.x, self.y, self.z):
            if not math.isfinite(float(value)):
                raise ValueError("Las coordenadas del muro deben ser finitas")
        object.__setattr__(self, "x", float(self.x))
        object.__setattr__(self, "y", float(self.y))
        object.__setattr__(self, "z", float(self.z))

    @classmethod
    def from_value(cls, value: "WallPoint | Iterable[float] | Any") -> "WallPoint":
        if isinstance(value, cls):
            return value
        if all(hasattr(value, name) for name in ("x", "y", "z")):
            return cls(value.x, value.y, value.z)
        coordinates = tuple(value)
        if len(coordinates) == 2:
            return cls(coordinates[0], coordinates[1], 0.0)
        if len(coordinates) == 3:
            return cls(*coordinates)
        raise ValueError("Un punto de muro requiere 2 o 3 coordenadas")

    def distance_to(self, other: "WallPoint") -> float:
        return math.sqrt(
            (self.x - other.x) ** 2
            + (self.y - other.y) ** 2
            + (self.z - other.z) ** 2
        )

    def to_tuple(self) -> tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass(frozen=True)
class WallLayer:
    name: str
    thickness: float
    material: MaterialRef | None = None
    function: str = "core"
    metadata: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        clean_name = str(self.name).strip()
        clean_function = str(self.function).strip()
        thickness = float(self.thickness)
        if not clean_name:
            raise ValueError("El nombre de la capa no puede estar vacío")
        if not clean_function:
            raise ValueError("La función de la capa no puede estar vacía")
        if not math.isfinite(thickness) or thickness <= 0:
            raise ValueError("El espesor de la capa debe ser positivo y finito")
        object.__setattr__(self, "name", clean_name)
        object.__setattr__(self, "function", clean_function)
        object.__setattr__(self, "thickness", thickness)
        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata or {})),
        )


class Wall(BimObject):
    IFC_CLASS = "IfcWall"

    def __init__(
        self,
        start: WallPoint | Iterable[float] | Any,
        end: WallPoint | Iterable[float] | Any,
        *,
        height: float = 3.0,
        thickness: float = 0.20,
        base_elevation: float = 0.0,
        name: str = "Muro",
        object_id: ObjectId | str | None = None,
        layers: Iterable[WallLayer] | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(
            name,
            ObjectType.WALL,
            object_id=object_id,
            metadata=metadata,
        )
        self._start = WallPoint.from_value(start)
        self._end = WallPoint.from_value(end)
        self._height = self._positive_finite(height, "height")
        self._thickness = self._positive_finite(thickness, "thickness")
        self._base_elevation = self._finite(base_elevation, "base_elevation")
        self._layers: tuple[WallLayer, ...] = ()
        self._validate_axis(self._start, self._end)
        if layers is not None:
            self._layers = self._validated_layers(tuple(layers), self._thickness)
        self._sync_properties()

    @staticmethod
    def _finite(value: float, field_name: str) -> float:
        number = float(value)
        if not math.isfinite(number):
            raise ValueError(f"{field_name} debe ser finito")
        return number

    @classmethod
    def _positive_finite(cls, value: float, field_name: str) -> float:
        number = cls._finite(value, field_name)
        if number <= 0:
            raise ValueError(f"{field_name} debe ser mayor que cero")
        return number

    @staticmethod
    def _validate_axis(start: WallPoint, end: WallPoint) -> None:
        if start.distance_to(end) <= _EPSILON:
            raise ValueError("El eje del muro debe tener longitud positiva")

    @staticmethod
    def _validated_layers(
        layers: tuple[WallLayer, ...],
        thickness: float,
    ) -> tuple[WallLayer, ...]:
        if not layers:
            return ()
        total = sum(layer.thickness for layer in layers)
        if not math.isclose(total, thickness, rel_tol=0.0, abs_tol=1e-9):
            raise ValueError(
                "La suma de espesores de las capas debe coincidir "
                "con el espesor total del muro"
            )
        return layers

    @property
    def start(self) -> WallPoint:
        return self._start

    @property
    def end(self) -> WallPoint:
        return self._end

    @property
    def height(self) -> float:
        return self._height

    @property
    def thickness(self) -> float:
        return self._thickness

    @property
    def base_elevation(self) -> float:
        return self._base_elevation

    @property
    def layers(self) -> tuple[WallLayer, ...]:
        return self._layers

    @property
    def length(self) -> float:
        return self._start.distance_to(self._end)

    @property
    def gross_side_area(self) -> float:
        return self.length * self.height

    @property
    def footprint_area(self) -> float:
        return self.length * self.thickness

    @property
    def gross_volume(self) -> float:
        return self.length * self.height * self.thickness

    @property
    def top_elevation(self) -> float:
        return self.base_elevation + self.height

    @property
    def direction(self) -> tuple[float, float, float]:
        length = self.length
        return (
            (self.end.x - self.start.x) / length,
            (self.end.y - self.start.y) / length,
            (self.end.z - self.start.z) / length,
        )

    @property
    def midpoint(self) -> WallPoint:
        return WallPoint(
            (self.start.x + self.end.x) / 2.0,
            (self.start.y + self.end.y) / 2.0,
            (self.start.z + self.end.z) / 2.0,
        )

    def set_axis(
        self,
        start: WallPoint | Iterable[float] | Any,
        end: WallPoint | Iterable[float] | Any,
    ) -> bool:
        new_start = WallPoint.from_value(start)
        new_end = WallPoint.from_value(end)
        self._validate_axis(new_start, new_end)
        if new_start == self._start and new_end == self._end:
            return False
        self._start = new_start
        self._end = new_end
        self._sync_properties()
        self._touch()
        return True

    def set_height(self, value: float) -> bool:
        new_value = self._positive_finite(value, "height")
        if math.isclose(new_value, self._height, abs_tol=_EPSILON):
            return False
        self._height = new_value
        self._sync_properties()
        self._touch()
        return True

    def set_thickness(self, value: float, *, clear_layers: bool = False) -> bool:
        new_value = self._positive_finite(value, "thickness")
        if math.isclose(new_value, self._thickness, abs_tol=_EPSILON):
            return False
        if self._layers and not clear_layers:
            raise ValueError(
                "No se puede cambiar el espesor con capas activas; "
                "usa clear_layers=True o set_layers()"
            )
        self._thickness = new_value
        if clear_layers:
            self._layers = ()
        self._sync_properties()
        self._touch()
        return True

    def set_base_elevation(self, value: float) -> bool:
        new_value = self._finite(value, "base_elevation")
        if math.isclose(new_value, self._base_elevation, abs_tol=_EPSILON):
            return False
        self._base_elevation = new_value
        self._sync_properties()
        self._touch()
        return True

    def set_layers(self, layers: Iterable[WallLayer]) -> bool:
        new_layers = tuple(layers)
        validated = self._validated_layers(new_layers, self._thickness)
        if validated == self._layers:
            return False
        self._layers = validated
        self._sync_materials_from_layers()
        self._sync_properties()
        self._touch()
        return True

    def clear_layers(self) -> bool:
        if not self._layers:
            return False
        self._layers = ()
        self._sync_properties()
        self._touch()
        return True

    def _sync_materials_from_layers(self) -> None:
        for index, layer in enumerate(self._layers):
            if layer.material is None:
                continue
            role = f"wall_layer_{index}:{layer.function}"
            material = MaterialRef(
                layer.material.material_id,
                layer.material.name,
                role,
                layer.material.metadata,
            )
            self.materials.add(material)

    def _sync_properties(self) -> None:
        values = {
            "axis_start": self.start.to_tuple(),
            "axis_end": self.end.to_tuple(),
            "length": self.length,
            "height": self.height,
            "thickness": self.thickness,
            "base_elevation": self.base_elevation,
            "top_elevation": self.top_elevation,
            "gross_side_area": self.gross_side_area,
            "footprint_area": self.footprint_area,
            "gross_volume": self.gross_volume,
            "ifc_class": self.IFC_CLASS,
            "layer_count": len(self.layers),
        }
        for key, value in values.items():
            self.properties.set(key, value)

    def quantity_snapshot(self) -> Mapping[str, float]:
        return MappingProxyType({
            "length": self.length,
            "height": self.height,
            "thickness": self.thickness,
            "gross_side_area": self.gross_side_area,
            "footprint_area": self.footprint_area,
            "gross_volume": self.gross_volume,
        })

    def snapshot(self) -> Mapping[str, Any]:
        base = dict(super().snapshot())
        base["geometry"] = MappingProxyType({
            "start": self.start.to_tuple(),
            "end": self.end.to_tuple(),
            "direction": self.direction,
            "midpoint": self.midpoint.to_tuple(),
        })
        base["quantities"] = self.quantity_snapshot()
        base["layers"] = tuple(self.layers)
        base["ifc_class"] = self.IFC_CLASS
        return MappingProxyType(base)
