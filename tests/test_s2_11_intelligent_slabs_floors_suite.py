import pytest

from engines.bim.slabs import (
    IntelligentSlab,
    IntelligentSlabEngine,
    Point2D,
    SlabKind,
    SlabLayer,
    SlabLayerFunction,
    SlabOpening,
    SlabStructure,
    SlabType,
    SlabTypeCatalog,
    SlabValidator,
    point_in_polygon,
    polygon_area,
    polygon_perimeter,
    slab_parameter_definitions,
)


def rect(width, height):
    return (
        Point2D(0, 0),
        Point2D(width, 0),
        Point2D(width, height),
        Point2D(0, height),
    )


@pytest.mark.parametrize("function", list(SlabLayerFunction))
def test_layer_functions(function):
    thickness = 0.0 if function is SlabLayerFunction.MEMBRANE else 0.01
    layer = SlabLayer("l", "Layer", function, thickness)
    assert layer.function is function


@pytest.mark.parametrize("width,height", [
    (1, 1), (2, 1), (2, 2), (3, 2), (4, 3),
    (5, 4), (6, 5), (8, 6), (10, 8), (12, 10),
])
def test_polygon_area_rectangles(width, height):
    assert polygon_area(rect(width, height)) == pytest.approx(width * height)


@pytest.mark.parametrize("width,height", [
    (1, 1), (2, 1), (2, 2), (3, 2), (4, 3),
    (5, 4), (6, 5), (8, 6), (10, 8), (12, 10),
])
def test_polygon_perimeter_rectangles(width, height):
    assert polygon_perimeter(rect(width, height)) == pytest.approx(2 * (width + height))


@pytest.mark.parametrize("point,expected", [
    (Point2D(1, 1), True),
    (Point2D(0.1, 0.1), True),
    (Point2D(3.9, 2.9), True),
    (Point2D(-1, 1), False),
    (Point2D(5, 1), False),
    (Point2D(2, 4), False),
    (Point2D(10, 10), False),
    (Point2D(2, 1.5), True),
    (Point2D(0.5, 2.5), True),
    (Point2D(4.5, 2.5), False),
])
def test_point_in_polygon_cases(point, expected):
    assert point_in_polygon(point, rect(4, 3)) is expected


@pytest.mark.parametrize("thickness", [0.01, 0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30])
def test_structure_total_thickness(thickness):
    structure = SlabStructure((SlabLayer("l", "Layer", SlabLayerFunction.STRUCTURE, thickness),))
    assert structure.total_thickness == pytest.approx(thickness)


@pytest.mark.parametrize("count", range(1, 11))
def test_structure_multiple_layers(count):
    layers = tuple(
        SlabLayer(f"l{i}", f"Layer {i}", SlabLayerFunction.STRUCTURE, 0.01)
        for i in range(count)
    )
    structure = SlabStructure(layers)
    assert structure.structural_thickness == pytest.approx(count * 0.01)


@pytest.mark.parametrize("kind", list(SlabKind))
def test_slab_kinds(kind):
    structure = SlabStructure((SlabLayer("l", "Layer", SlabLayerFunction.STRUCTURE, 0.2),))
    slab_type = SlabType("t", "Type", structure, kind=kind)
    assert slab_type.kind is kind


@pytest.mark.parametrize("elevation", [0, 0.1, 1, 2, 3, 5, 10, -1, -3, 100])
def test_slab_elevation(elevation):
    slab = IntelligentSlab("s", "t", rect(4, 3), elevation=elevation)
    assert slab.elevation == elevation


@pytest.mark.parametrize("slope", [0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.1, 0.15, 0.2])
def test_slab_slopes(slope):
    slab = IntelligentSlab("s", "t", rect(4, 3), slope=slope)
    assert slab.slope == slope


@pytest.mark.parametrize("index", range(10))
def test_catalog_register_remove(index):
    catalog = SlabTypeCatalog()
    structure = SlabStructure((SlabLayer("l", "Layer", SlabLayerFunction.STRUCTURE, 0.2),))
    slab_type = SlabType(f"t{index}", f"Type {index}", structure)
    catalog.register(slab_type)
    assert catalog.get(slab_type.type_id) is slab_type
    assert catalog.remove(slab_type.type_id) is slab_type


def make_engine():
    engine = IntelligentSlabEngine()
    structure = SlabStructure((
        SlabLayer("finish", "Finish", SlabLayerFunction.FINISH, 0.03),
        SlabLayer("core", "Core", SlabLayerFunction.STRUCTURE, 0.20),
        SlabLayer("ceiling", "Ceiling", SlabLayerFunction.FINISH, 0.02),
    ))
    engine.register_type(SlabType("floor", "Floor", structure))
    return engine


def test_validation_errors():
    with pytest.raises(ValueError):
        Point2D(float("inf"), 0)
    with pytest.raises(ValueError):
        SlabStructure(())
    with pytest.raises(ValueError):
        IntelligentSlab("", "t", rect(1, 1))


def test_validator_accepts_valid_slab():
    slab = IntelligentSlab("s", "t", rect(4, 3))
    assert SlabValidator().validate(slab).valid


def test_validator_rejects_outside_opening():
    slab = IntelligentSlab(
        "s",
        "t",
        rect(4, 3),
        openings=(SlabOpening("o", (Point2D(3, 2), Point2D(5, 2), Point2D(5, 4), Point2D(3, 4))),),
    )
    assert not SlabValidator().validate(slab).valid


def test_engine_add_remove_slab():
    engine = make_engine()
    slab = IntelligentSlab("s", "floor", rect(4, 3))
    engine.add_slab(slab)
    assert engine.remove_slab("s") is slab


def test_engine_change_type():
    engine = make_engine()
    structure = SlabStructure((SlabLayer("core2", "Core2", SlabLayerFunction.STRUCTURE, 0.30),))
    engine.register_type(SlabType("thick", "Thick", structure))
    engine.add_slab(IntelligentSlab("s", "floor", rect(4, 3)))
    engine.change_type("s", "thick")
    assert engine.get_slab("s").slab_type_id == "thick"


def test_engine_add_remove_opening():
    engine = make_engine()
    engine.add_slab(IntelligentSlab("s", "floor", rect(8, 6)))
    opening = SlabOpening("o", rect(2, 2))
    engine.add_opening("s", opening)
    assert engine.get_slab("s").openings == (opening,)
    engine.remove_opening("s", "o")
    assert engine.get_slab("s").openings == ()


def test_engine_set_slope():
    engine = make_engine()
    engine.add_slab(IntelligentSlab("s", "floor", rect(4, 3)))
    engine.set_slope("s", 0.02, 90)
    slab = engine.get_slab("s")
    assert slab.slope == 0.02
    assert slab.slope_direction_degrees == 90


def test_quantities_with_opening():
    engine = make_engine()
    engine.add_slab(IntelligentSlab("s", "floor", rect(8, 6)))
    engine.add_opening("s", SlabOpening("o", (Point2D(2, 2), Point2D(4, 2), Point2D(4, 4), Point2D(2, 4))))
    q = engine.calculate_quantities("s")
    assert q.gross_area == pytest.approx(48)
    assert q.opening_area == pytest.approx(4)
    assert q.net_area == pytest.approx(44)
    assert q.volume == pytest.approx(11)


def test_parameter_definitions():
    ids = {definition.parameter_id for definition in slab_parameter_definitions()}
    assert {"elevation", "slope", "gross_area", "net_area", "volume"} <= ids


def test_events():
    events = []
    engine = IntelligentSlabEngine(event_dispatcher=lambda name, payload: events.append((name, payload)))
    structure = SlabStructure((SlabLayer("core", "Core", SlabLayerFunction.STRUCTURE, 0.2),))
    engine.register_type(SlabType("t", "Type", structure))
    engine.add_slab(IntelligentSlab("s", "t", rect(4, 3)))
    assert events[0][0] == "slab.type.registered"
    assert events[-1][0] == "slab.added"


@pytest.mark.parametrize("index", range(21))
def test_additional_slab_catalog_cases(index):
    catalog = SlabTypeCatalog()
    structure = SlabStructure((
        SlabLayer("core", "Core", SlabLayerFunction.STRUCTURE, 0.20),
    ))
    slab_type = SlabType(f"extra-{index}", f"Extra {index}", structure)
    catalog.register(slab_type)
    assert catalog.get(slab_type.type_id) is slab_type
