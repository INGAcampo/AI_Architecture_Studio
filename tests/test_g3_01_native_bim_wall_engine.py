import pytest

from bim_authoring.walls import (
    CompoundStructure,
    NativeBimWallEngine,
    WallInstance,
    WallJoin,
    WallJoinType,
    WallLayer,
    WallLocationLine,
    WallOpening,
    WallProfile,
    WallType,
)


def make_wall(index=0):
    structure = CompoundStructure((
        WallLayer("finish-ext", "plaster", 0.02, "finish"),
        WallLayer("core", "concrete", 0.16, "structure"),
        WallLayer("finish-int", "paint", 0.01, "finish"),
    ))
    wall_type = WallType(
        "WT-01",
        "Concrete Wall 190",
        structure,
        fire_rating_minutes=120,
        thermal_resistance=2.4,
    )
    profile = WallProfile(
        (0.0, 0.0, 0.0),
        (5.0 + index * 0.01, 0.0, 0.0),
        0.0,
        3.0,
    )
    return WallInstance(
        f"W-{index}",
        wall_type,
        profile,
        WallLocationLine.CENTERLINE,
        level_id="L1",
    )


@pytest.mark.parametrize("i", range(20))
def test_wall_model(i):
    wall = make_wall(i)
    assert wall.profile.length == pytest.approx(5 + i * 0.01)
    assert wall.wall_type.structure.total_thickness == pytest.approx(0.19)
    assert wall.wall_type.fire_rating_minutes == 120


@pytest.mark.parametrize("i", range(20))
def test_geometry(i):
    engine = NativeBimWallEngine()
    wall = make_wall(i)
    engine.add_wall(wall)
    result = engine.regenerate(wall.wall_id)
    assert len(result.geometry.vertices) == 8
    assert len(result.geometry.faces) == 6
    assert result.geometry.height == 3.0


@pytest.mark.parametrize("i", range(20))
def test_openings(i):
    engine = NativeBimWallEngine()
    wall = make_wall(i)
    engine.add_wall(wall)
    opening = WallOpening(
        f"O-{i}",
        wall.wall_id,
        1.0,
        0.9,
        0.0,
        2.1,
        hosted_element_id=f"D-{i}",
    )
    engine.add_opening(opening)
    quantities = engine.quantities(wall.wall_id)
    assert quantities.opening_area == pytest.approx(1.89)
    assert quantities.net_area < quantities.gross_area


@pytest.mark.parametrize("i", range(20))
def test_joins(i):
    engine = NativeBimWallEngine()
    a = make_wall(i)
    b = make_wall(i + 1)
    engine.add_wall(a)
    engine.add_wall(b)
    join = WallJoin(f"J-{i}", a.wall_id, b.wall_id, WallJoinType.MITER)
    engine.joins.connect(join)
    assert engine.joins.for_wall(a.wall_id) == (join,)


@pytest.mark.parametrize("i", range(20))
def test_regeneration(i):
    engine = NativeBimWallEngine()
    wall = make_wall(i)
    engine.add_wall(wall)
    updated = wall.with_profile(
        WallProfile(
            wall.profile.start,
            (7.0, 0.0, 0.0),
            wall.profile.base_elevation,
            3.2,
        )
    )
    result = engine.update_wall(updated)
    assert result.new_revision == 1
    assert result.geometry.length == pytest.approx(7.0)
    assert result.quantities.height == pytest.approx(3.2)


@pytest.mark.parametrize("i", range(20))
def test_validation_and_quantities(i):
    engine = NativeBimWallEngine()
    wall = make_wall(i)
    engine.add_wall(wall)
    quantities = engine.quantities(wall.wall_id)
    assert quantities.gross_area == pytest.approx(wall.profile.length * 3.0)
    assert quantities.gross_volume == pytest.approx(
        quantities.gross_area * 0.19
    )
    assert engine.regenerate(wall.wall_id).issues == ()
