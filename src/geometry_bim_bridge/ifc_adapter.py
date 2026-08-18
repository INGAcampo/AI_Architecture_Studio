from __future__ import annotations

from pathlib import Path

from .contracts import BridgeEntityRef


def require_ifcopenshell():
    try:
        import ifcopenshell
    except Exception as exc:
        raise RuntimeError("IfcOpenShell runtime is not available") from exc
    return ifcopenshell


def open_ifc(path: str | Path):
    ifcopenshell = require_ifcopenshell()
    return ifcopenshell.open(str(path))


def entity_ref(entity) -> BridgeEntityRef:
    entity_type = entity.is_a()
    entity_id = str(entity.id())
    global_id = getattr(entity, "GlobalId", None)
    return BridgeEntityRef(
        source="IFC",
        entity_id=entity_id,
        entity_type=entity_type,
        global_id=global_id,
    )


def create_minimal_wall_model():
    ifcopenshell = require_ifcopenshell()
    model = ifcopenshell.file(schema="IFC4")
    project = model.create_entity(
        "IfcProject",
        GlobalId=ifcopenshell.guid.new(),
        Name="AIAS Shadow Bridge Project",
    )
    site = model.create_entity(
        "IfcSite",
        GlobalId=ifcopenshell.guid.new(),
        Name="AIAS Shadow Bridge Site",
    )
    building = model.create_entity(
        "IfcBuilding",
        GlobalId=ifcopenshell.guid.new(),
        Name="AIAS Shadow Bridge Building",
    )
    storey = model.create_entity(
        "IfcBuildingStorey",
        GlobalId=ifcopenshell.guid.new(),
        Name="AIAS Shadow Bridge Storey",
    )
    wall = model.create_entity(
        "IfcWall",
        GlobalId=ifcopenshell.guid.new(),
        Name="AIAS Shadow Bridge Wall",
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
    model.create_entity(
        "IfcRelContainedInSpatialStructure",
        GlobalId=ifcopenshell.guid.new(),
        RelatingStructure=storey,
        RelatedElements=[wall],
    )

    return model, wall
