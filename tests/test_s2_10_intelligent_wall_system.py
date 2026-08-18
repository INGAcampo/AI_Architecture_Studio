import pytest

from engines.bim.walls import (
    CompoundStructure,
    IntelligentWall,
    IntelligentWallEngine,
    WallJoin,
    WallJoinEngine,
    WallJoinKind,
    WallLayer,
    WallLayerFunction,
    WallLocationLine,
    WallQuantityCalculator,
    WallType,
    WallTypeCatalog,
    wall_parameter_definitions,
)


@pytest.mark.parametrize("function", list(WallLayerFunction))
def test_layer_functions(function):
    thickness = 0.0 if function is WallLayerFunction.MEMBRANE else 0.01
    layer = WallLayer("l", "Layer", function, thickness)
    assert layer.function is function


@pytest.mark.parametrize("thickness", [0.01, 0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30])
def test_compound_total_thickness(thickness):
    structure = CompoundStructure((WallLayer("l", "Layer", WallLayerFunction.STRUCTURE, thickness),))
    assert structure.total_thickness == pytest.approx(thickness)


@pytest.mark.parametrize("count", range(1, 11))
def test_compound_multiple_layers(count):
    layers = tuple(
        WallLayer(f"l{i}", f"Layer {i}", WallLayerFunction.STRUCTURE, 0.01)
        for i in range(count)
    )
    structure = CompoundStructure(layers)
    assert structure.total_thickness == pytest.approx(count * 0.01)


@pytest.mark.parametrize("count", range(1, 11))
def test_core_thickness(count):
    layers = tuple(
        WallLayer(f"l{i}", f"Core {i}", WallLayerFunction.STRUCTURE, 0.02)
        for i in range(count)
    )
    structure = CompoundStructure(layers)
    assert structure.core_thickness == pytest.approx(count * 0.02)


@pytest.mark.parametrize("minutes", [0, 30, 45, 60, 90, 120, 180, 240, 300, 360])
def test_wall_type_fire_rating(minutes):
    structure = CompoundStructure((WallLayer("l", "Core", WallLayerFunction.STRUCTURE, 0.2),))
    wall_type = WallType("t", "Type", structure, fire_rating_minutes=minutes)
    assert wall_type.fire_rating_minutes == minutes


@pytest.mark.parametrize("length", [1, 2, 3, 4, 5, 6, 8, 10, 12, 20])
def test_wall_lengths(length):
    wall = IntelligentWall("w", "t", length, 0, 3)
    assert wall.length == length


@pytest.mark.parametrize("location_line", list(WallLocationLine))
def test_location_lines(location_line):
    wall = IntelligentWall("w", "t", 5, 0, 3, location_line=location_line)
    assert wall.location_line is location_line


@pytest.mark.parametrize("height,expected", [
    (2.4, 2.4), (2.7, 2.7), (3.0, 3.0), (3.3, 3.3), (3.6, 3.6),
    (4.0, 4.0), (4.5, 4.5), (5.0, 5.0), (6.0, 6.0), (10.0, 10.0),
])
def test_top_elevation(height, expected):
    wall = IntelligentWall("w", "t", 5, 0, height)
    assert wall.top_elevation == pytest.approx(expected)


@pytest.mark.parametrize("index", range(10))
def test_catalog_register_remove(index):
    catalog = WallTypeCatalog()
    structure = CompoundStructure((WallLayer("l", "Core", WallLayerFunction.STRUCTURE, 0.2),))
    wall_type = WallType(f"t{index}", f"Type {index}", structure)
    catalog.register(wall_type)
    assert catalog.get(wall_type.type_id) is wall_type
    assert catalog.remove(wall_type.type_id) is wall_type


@pytest.mark.parametrize("index", range(10))
def test_catalog_duplicate(index):
    catalog = WallTypeCatalog()
    structure = CompoundStructure((WallLayer("l", "Core", WallLayerFunction.STRUCTURE, 0.2),))
    wall_type = WallType("source", "Source", structure)
    catalog.register(wall_type)
    duplicate = catalog.duplicate("source", f"copy{index}", f"Copy {index}")
    assert duplicate.type_id == f"copy{index}"


@pytest.mark.parametrize("kind", list(WallJoinKind))
def test_join_kinds(kind):
    join = WallJoin("j", ("a", "b"), kind)
    assert join.kind is kind


def make_engine():
    engine = IntelligentWallEngine()
    structure = CompoundStructure((
        WallLayer("ext", "Exterior", WallLayerFunction.FINISH, 0.02),
        WallLayer("core", "Core", WallLayerFunction.STRUCTURE, 0.16),
        WallLayer("int", "Interior", WallLayerFunction.FINISH, 0.02),
    ))
    engine.register_type(WallType("basic", "Basic", structure))
    return engine


def test_model_validation():
    with pytest.raises(ValueError):
        WallLayer("", "Layer", WallLayerFunction.STRUCTURE, 0.1)
    with pytest.raises(ValueError):
        CompoundStructure(())
    with pytest.raises(ValueError):
        IntelligentWall("", "t", 1, 0, 3)


def test_engine_add_remove_wall():
    engine = make_engine()
    wall = IntelligentWall("w", "basic", 5, 0, 3)
    engine.add_wall(wall)
    assert engine.remove_wall("w") is wall


def test_engine_change_type():
    engine = make_engine()
    structure = CompoundStructure((WallLayer("c", "Core", WallLayerFunction.STRUCTURE, 0.3),))
    engine.register_type(WallType("thick", "Thick", structure))
    engine.add_wall(IntelligentWall("w", "basic", 5, 0, 3))
    engine.change_type("w", "thick")
    assert engine.get_wall("w").wall_type_id == "thick"


def test_engine_resize():
    engine = make_engine()
    engine.add_wall(IntelligentWall("w", "basic", 5, 0, 3))
    engine.resize("w", length=8, height=4)
    assert engine.get_wall("w").length == 8
    assert engine.get_wall("w").height == 4


def test_engine_flip():
    engine = make_engine()
    engine.add_wall(IntelligentWall("w", "basic", 5, 0, 3))
    engine.flip("w")
    assert engine.get_wall("w").flipped


def test_engine_join():
    engine = make_engine()
    engine.add_wall(IntelligentWall("a", "basic", 5, 0, 3))
    engine.add_wall(IntelligentWall("b", "basic", 5, 0, 3))
    join = engine.create_join(WallJoin("j", ("a", "b"), WallJoinKind.L))
    assert join.wall_ids == ("a", "b")
    assert engine.clean_join("j").cleaned


def test_quantities():
    engine = make_engine()
    engine.add_wall(IntelligentWall("w", "basic", 5, 0, 3))
    q = engine.calculate_quantities("w")
    assert q.gross_area == pytest.approx(15)
    assert q.volume == pytest.approx(3)
    assert q.core_volume == pytest.approx(2.4)


def test_parameter_definitions():
    ids = {definition.parameter_id for definition in wall_parameter_definitions()}
    assert {"length", "height", "gross_area", "net_area", "volume"} <= ids


def test_events():
    events = []
    engine = IntelligentWallEngine(event_dispatcher=lambda name, payload: events.append((name, payload)))
    structure = CompoundStructure((WallLayer("c", "Core", WallLayerFunction.STRUCTURE, 0.2),))
    engine.register_type(WallType("t", "Type", structure))
    engine.add_wall(IntelligentWall("w", "t", 5, 0, 3))
    assert events[0][0] == "wall.type.registered"
    assert events[-1][0] == "wall.added"


@pytest.mark.parametrize("index", range(8))
def test_engine_many_walls(index):
    engine = make_engine()
    wall = IntelligentWall(f"w{index}", "basic", 5 + index, 0, 3)
    engine.add_wall(wall)
    assert engine.get_wall(wall.wall_id) is wall


@pytest.mark.parametrize("index", range(6))
def test_wall_type_catalog_additional_cases(index):
    catalog = WallTypeCatalog()
    structure = CompoundStructure((
        WallLayer("core", "Core", WallLayerFunction.STRUCTURE, 0.20),
    ))
    wall_type = WallType(f"extra-{index}", f"Extra {index}", structure)
    catalog.register(wall_type)
    assert catalog.get(wall_type.type_id) is wall_type
