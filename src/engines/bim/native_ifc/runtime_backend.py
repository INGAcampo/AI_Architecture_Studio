from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class IfcRuntimeInfo:
    available: bool
    version: str | None
    origin: str | None


class IfcOpenShellRuntimeBackend:
    """Lazy IfcOpenShell runtime for AIAS Wave 2."""

    @staticmethod
    def discover() -> IfcRuntimeInfo:
        try:
            import ifcopenshell
        except Exception:
            return IfcRuntimeInfo(False, None, None)
        return IfcRuntimeInfo(
            True,
            getattr(ifcopenshell, "version", None),
            getattr(ifcopenshell, "__file__", None),
        )

    @staticmethod
    def _require() -> Any:
        try:
            import ifcopenshell
        except Exception as exc:
            raise RuntimeError("IfcOpenShell runtime is not available") from exc
        return ifcopenshell

    def create_minimal_project(self, schema: str = "IFC4"):
        ifcopenshell = self._require()
        model = ifcopenshell.file(schema=schema)
        project = model.create_entity(
            "IfcProject",
            GlobalId=ifcopenshell.guid.new(),
            Name="AIAS Project",
        )
        return model, project

    def add_spatial_hierarchy(self, model):
        ifcopenshell = self._require()
        project = model.by_type("IfcProject")[0]
        site = model.create_entity(
            "IfcSite", GlobalId=ifcopenshell.guid.new(), Name="AIAS Site"
        )
        building = model.create_entity(
            "IfcBuilding", GlobalId=ifcopenshell.guid.new(), Name="AIAS Building"
        )
        storey = model.create_entity(
            "IfcBuildingStorey",
            GlobalId=ifcopenshell.guid.new(),
            Name="AIAS Storey",
        )
        model.create_entity(
            "IfcRelAggregates",
            GlobalId=ifcopenshell.guid.new(),
            RelatingObject=project,
            RelatedObjects=[site],
        )
        model.create_entity(
            "IfcRelAggregates",
            GlobalId=ifcopenshell.guid.new(),
            RelatingObject=site,
            RelatedObjects=[building],
        )
        model.create_entity(
            "IfcRelAggregates",
            GlobalId=ifcopenshell.guid.new(),
            RelatingObject=building,
            RelatedObjects=[storey],
        )
        return site, building, storey

    def add_wall(self, model, storey, name: str = "AIAS Wall"):
        ifcopenshell = self._require()
        wall = model.create_entity(
            "IfcWall", GlobalId=ifcopenshell.guid.new(), Name=name
        )
        model.create_entity(
            "IfcRelContainedInSpatialStructure",
            GlobalId=ifcopenshell.guid.new(),
            RelatingStructure=storey,
            RelatedElements=[wall],
        )
        return wall

    def write(self, model, path: str | Path) -> None:
        model.write(str(path))

    def open(self, path: str | Path):
        ifcopenshell = self._require()
        return ifcopenshell.open(str(path))
