import pytest

from bim_authoring.windows import (
    NativeBimWindowEngine,
    WindowFamily,
    WindowFrame,
    WindowGlass,
    WindowInstance,
    WindowOperation,
    WindowType,
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
        CompoundStructure((WallLayer("L1", "concrete", 0.20, "structure"),)),
    )
    wall_engine.add_wall(
        WallInstance(
            "W1",
            wall_type,
            WallProfile((0,0,0), (6,0,0), 0, 3),
            level_id="L1",
        )
    )
    return wall_engine


def make_family():
    window_type = WindowType(
        "WIN-1200x1200",
        "1200x1200 Casement",
        1.20,
        1.20,
        WindowOperation.CASEMENT,
        WindowFrame("FR1", "aluminum", 0.20, 0.05),
        WindowGlass("GL1", "double_glazing", 0.024, 1.8, 0.45),
        mullion_count_vertical=1,
        mullion_count_horizontal=1,
    )
    return WindowFamily("WF1", "Standard Windows", (window_type,))


@pytest.mark.parametrize("i", range(20))
def test_family_and_type(i):
    family = make_family()
    window_type = family.get_type("WIN-1200x1200")
    assert window_type.width == 1.20
    assert window_type.height == 1.20
    assert window_type.glass.u_value == 1.8


@pytest.mark.parametrize("i", range(20))
def test_geometry(i):
    family = make_family()
    engine = NativeBimWindowEngine()
    engine.register_family(family)
    window = WindowInstance(
        f"WIN-{i}",
        family.family_id,
        family.types[0],
        "W1",
        1.0,
        0.9,
    )
    engine.add_window(window, auto_host=False)
    result = engine.regenerate(window.window_id)
    assert len(result.geometry.frame_vertices) == 4
    assert len(result.geometry.glass_vertices) == 4
    assert len(result.geometry.mullions) == 2


@pytest.mark.parametrize("i", range(20))
def test_hosting(i):
    wall_engine = make_wall_engine()
    family = make_family()
    engine = NativeBimWindowEngine(wall_engine)
    engine.register_family(family)
    window = WindowInstance(
        f"WIN-{i}",
        family.family_id,
        family.types[0],
        "W1",
        1.0,
        0.9,
    )
    engine.add_window(window)
    openings = wall_engine.openings.for_wall("W1")
    assert len(openings) == 1
    assert openings[0].hosted_element_id == window.window_id


@pytest.mark.parametrize("i", range(20))
def test_quantities(i):
    family = make_family()
    engine = NativeBimWindowEngine()
    engine.register_family(family)
    window = WindowInstance(
        f"WIN-{i}",
        family.family_id,
        family.types[0],
        "W1",
        0.5,
        0.9,
    )
    engine.add_window(window, auto_host=False)
    quantities = engine.quantities(window.window_id, delta_temperature=10)
    assert quantities.opening_area == pytest.approx(1.44)
    assert quantities.glass_area == pytest.approx(1.21)
    assert quantities.estimated_heat_transfer == pytest.approx(25.92)


@pytest.mark.parametrize("i", range(20))
def test_regeneration(i):
    family = make_family()
    engine = NativeBimWindowEngine()
    engine.register_family(family)
    window = WindowInstance(
        f"WIN-{i}",
        family.family_id,
        family.types[0],
        "W1",
        0.5,
        0.9,
    )
    engine.add_window(window, auto_host=False)
    updated = window.move(offset=1.5, sill_height=1.0)
    result = engine.update_window(updated)
    assert result.new_revision == 1
    assert result.geometry.frame_vertices[0][0] == pytest.approx(1.5)
    assert result.geometry.frame_vertices[0][2] == pytest.approx(1.0)


@pytest.mark.parametrize("i", range(20))
def test_validation(i):
    wall_engine = make_wall_engine()
    family = make_family()
    engine = NativeBimWindowEngine(wall_engine)
    engine.register_family(family)
    window = WindowInstance(
        f"WIN-{i}",
        family.family_id,
        family.types[0],
        "W1",
        1.0,
        0.9,
    )
    engine.add_window(window)
    result = engine.regenerate(window.window_id)
    assert result.issues == ()
