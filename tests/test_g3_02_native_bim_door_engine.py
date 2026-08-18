import pytest

from bim_authoring.doors import (
    DoorFamily,
    DoorFrame,
    DoorHanding,
    DoorInstance,
    DoorOperation,
    DoorPanel,
    DoorType,
    NativeBimDoorEngine,
)
from bim_authoring.walls import (
    CompoundStructure,
    NativeBimWallEngine,
    WallInstance,
    WallLayer,
    WallProfile,
    WallType,
)


def make_wall_engine():
    wall_engine = NativeBimWallEngine()
    wall_type = WallType(
        "WT1",
        "Basic Wall",
        CompoundStructure((
            WallLayer("L1", "concrete", 0.20, "structure"),
        )),
    )
    wall = WallInstance(
        "W1",
        wall_type,
        WallProfile((0,0,0), (6,0,0), 0, 3),
        level_id="L1",
    )
    wall_engine.add_wall(wall)
    return wall_engine


def make_family():
    door_type = DoorType(
        "DT-900",
        "900x2100",
        0.90,
        2.10,
        DoorOperation.SINGLE_SWING,
        DoorHanding.LEFT,
        DoorPanel("P1", "wood", 0.045),
        DoorFrame("F1", "aluminum", 0.20, 0.05),
        fire_rating_minutes=60,
        acoustic_rating_db=32,
    )
    return DoorFamily("DF1", "Single Doors", (door_type,))


@pytest.mark.parametrize("i", range(20))
def test_family_and_type(i):
    family = make_family()
    door_type = family.get_type("DT-900")
    assert door_type.width == 0.90
    assert door_type.height == 2.10
    assert door_type.fire_rating_minutes == 60


@pytest.mark.parametrize("i", range(20))
def test_geometry(i):
    family = make_family()
    door = DoorInstance(
        f"D{i}",
        family.family_id,
        family.types[0],
        "W1",
        1.0,
    )
    engine = NativeBimDoorEngine()
    engine.register_family(family)
    engine.add_door(door, auto_host=False)
    result = engine.regenerate(door.door_id)
    assert len(result.geometry.frame_vertices) == 4
    assert len(result.geometry.swing_arc) == 7
    assert result.geometry.width == pytest.approx(0.9)


@pytest.mark.parametrize("i", range(20))
def test_hosting(i):
    wall_engine = make_wall_engine()
    family = make_family()
    door_engine = NativeBimDoorEngine(wall_engine)
    door_engine.register_family(family)
    door = DoorInstance(
        f"D{i}",
        family.family_id,
        family.types[0],
        "W1",
        1.0,
    )
    door_engine.add_door(door)
    openings = wall_engine.openings.for_wall("W1")
    assert len(openings) == 1
    assert openings[0].hosted_element_id == door.door_id


@pytest.mark.parametrize("i", range(20))
def test_quantities(i):
    family = make_family()
    engine = NativeBimDoorEngine()
    engine.register_family(family)
    door = DoorInstance(f"D{i}", family.family_id, family.types[0], "W1", 0.5)
    engine.add_door(door, auto_host=False)
    quantities = engine.quantities(door.door_id)
    assert quantities.opening_area == pytest.approx(1.89)
    assert quantities.panel_volume == pytest.approx(1.89 * 0.045)


@pytest.mark.parametrize("i", range(20))
def test_regeneration(i):
    family = make_family()
    engine = NativeBimDoorEngine()
    engine.register_family(family)
    door = DoorInstance(f"D{i}", family.family_id, family.types[0], "W1", 0.5)
    engine.add_door(door, auto_host=False)
    updated = door.move(1.5)
    result = engine.update_door(updated)
    assert result.new_revision == 1
    assert result.geometry.frame_vertices[0][0] == pytest.approx(1.5)


@pytest.mark.parametrize("i", range(20))
def test_validation(i):
    wall_engine = make_wall_engine()
    family = make_family()
    engine = NativeBimDoorEngine(wall_engine)
    engine.register_family(family)
    door = DoorInstance(f"D{i}", family.family_id, family.types[0], "W1", 1.0)
    engine.add_door(door)
    result = engine.regenerate(door.door_id)
    assert result.issues == ()
