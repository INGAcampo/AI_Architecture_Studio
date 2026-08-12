import pytest

from engines.bim.roofs import (
    IntelligentRoof,
    IntelligentRoofEngine,
    RoofKind,
    RoofLayer,
    RoofLayerFunction,
    RoofOpening,
    RoofPoint,
    RoofStructure,
    RoofType,
    RoofTypeCatalog,
    RoofValidator,
    polygon_area,
    polygon_perimeter,
    roof_parameter_definitions,
    sloped_area,
)


def rect(width, height):
    return (
        RoofPoint(0, 0),
        RoofPoint(width, 0),
        RoofPoint(width, height),
        RoofPoint(0, height),
    )


@pytest.mark.parametrize("function", list(RoofLayerFunction))
def test_layer_functions(function):
    thickness = 0.0 if function is RoofLayerFunction.MEMBRANE else 0.01
    assert RoofLayer("l", "Layer", function, thickness).function is function


@pytest.mark.parametrize("kind", list(RoofKind))
def test_roof_kinds(kind):
    structure = RoofStructure((RoofLayer("l", "Core", RoofLayerFunction.STRUCTURE, 0.2),))
    assert RoofType("t", "Type", structure, kind=kind).kind is kind


@pytest.mark.parametrize("width,height", [
    (1, 1), (2, 1), (2, 2), (3, 2), (4, 3),
    (5, 4), (6, 5), (8, 6), (10, 8), (12, 10),
])
def test_projected_area(width, height):
    assert polygon_area(rect(width, height)) == pytest.approx(width * height)


@pytest.mark.parametrize("width,height", [
    (1, 1), (2, 1), (2, 2), (3, 2), (4, 3),
    (5, 4), (6, 5), (8, 6), (10, 8), (12, 10),
])
def test_eave_perimeter(width, height):
    assert polygon_perimeter(rect(width, height)) == pytest.approx(2 * (width + height))


@pytest.mark.parametrize("pitch", [0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
def test_sloped_area_increases(pitch):
    area = sloped_area(100, pitch)
    assert area >= 100


@pytest.mark.parametrize("thickness", [0.01, 0.02, 0.05, 0.08, 0.10, 0.12, 0.15, 0.20, 0.25, 0.30])
def test_structure_total_thickness(thickness):
    structure = RoofStructure((RoofLayer("l", "Core", RoofLayerFunction.STRUCTURE, thickness),))
    assert structure.total_thickness == pytest.approx(thickness)


@pytest.mark.parametrize("count", range(1, 11))
def test_structural_thickness(count):
    layers = tuple(
        RoofLayer(f"l{i}", f"Core {i}", RoofLayerFunction.STRUCTURE, 0.01)
        for i in range(count)
    )
    assert RoofStructure(layers).structural_thickness == pytest.approx(count * 0.01)


@pytest.mark.parametrize("pitch", [0, 5, 10, 15, 20, 25, 30, 35, 40, 45])
def test_roof_pitch_values(pitch):
    roof = IntelligentRoof("r", "t", rect(4, 3), pitch_degrees=pitch)
    assert roof.pitch_degrees == pitch


@pytest.mark.parametrize("overhang", [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2])
def test_roof_overhang_values(overhang):
    roof = IntelligentRoof("r", "t", rect(4, 3), overhang=overhang)
    assert roof.overhang == overhang


@pytest.mark.parametrize("index", range(10))
def test_catalog_register_remove(index):
    catalog = RoofTypeCatalog()
    structure = RoofStructure((RoofLayer("l", "Core", RoofLayerFunction.STRUCTURE, 0.2),))
    roof_type = RoofType(f"t{index}", f"Type {index}", structure)
    catalog.register(roof_type)
    assert catalog.get(roof_type.type_id) is roof_type
    assert catalog.remove(roof_type.type_id) is roof_type


def make_engine():
    engine = IntelligentRoofEngine()
    structure = RoofStructure((
        RoofLayer("finish", "Finish", RoofLayerFunction.FINISH, 0.03),
        RoofLayer("core", "Core", RoofLayerFunction.STRUCTURE, 0.20),
        RoofLayer("ceiling", "Ceiling", RoofLayerFunction.CEILING, 0.02),
    ))
    engine.register_type(RoofType("gable", "Gable", structure, kind=RoofKind.GABLE))
    return engine


def test_model_validation():
    with pytest.raises(ValueError):
        RoofPoint(float("inf"), 0)
    with pytest.raises(ValueError):
        RoofStructure(())
    with pytest.raises(ValueError):
        IntelligentRoof("", "t", rect(1, 1))


def test_validator_accepts_valid_roof():
    roof = IntelligentRoof("r", "t", rect(4, 3))
    assert RoofValidator().validate(roof).valid


def test_validator_rejects_outside_opening():
    roof = IntelligentRoof(
        "r",
        "t",
        rect(4, 3),
        openings=(RoofOpening("o", (RoofPoint(3, 2), RoofPoint(5, 2), RoofPoint(5, 4), RoofPoint(3, 4))),),
    )
    assert not RoofValidator().validate(roof).valid


def test_engine_add_remove_roof():
    engine = make_engine()
    roof = IntelligentRoof("r", "gable", rect(4, 3))
    engine.add_roof(roof)
    assert engine.remove_roof("r") is roof


def test_engine_change_type():
    engine = make_engine()
    structure = RoofStructure((RoofLayer("core2", "Core2", RoofLayerFunction.STRUCTURE, 0.30),))
    engine.register_type(RoofType("thick", "Thick", structure))
    engine.add_roof(IntelligentRoof("r", "gable", rect(4, 3)))
    engine.change_type("r", "thick")
    assert engine.get_roof("r").roof_type_id == "thick"


def test_engine_set_pitch():
    engine = make_engine()
    engine.add_roof(IntelligentRoof("r", "gable", rect(4, 3)))
    engine.set_pitch("r", 30)
    assert engine.get_roof("r").pitch_degrees == 30


def test_engine_set_overhang():
    engine = make_engine()
    engine.add_roof(IntelligentRoof("r", "gable", rect(4, 3)))
    engine.set_overhang("r", 0.6)
    assert engine.get_roof("r").overhang == 0.6


def test_engine_add_remove_opening():
    engine = make_engine()
    engine.add_roof(IntelligentRoof("r", "gable", rect(8, 6)))
    opening = RoofOpening("o", (RoofPoint(2, 2), RoofPoint(4, 2), RoofPoint(4, 4), RoofPoint(2, 4)))
    engine.add_opening("r", opening)
    assert engine.get_roof("r").openings == (opening,)
    engine.remove_opening("r", "o")
    assert engine.get_roof("r").openings == ()


def test_quantities():
    engine = make_engine()
    engine.add_roof(
        IntelligentRoof(
            "r",
            "gable",
            rect(10, 8),
            pitch_degrees=30,
            overhang=0.5,
            ridge_length=10,
            valley_length=2,
            hip_length=4,
        )
    )
    q = engine.calculate_quantities("r")
    assert q.projected_area == pytest.approx(80)
    assert q.sloped_area > 80
    assert q.ridge_length == 10
    assert q.valley_length == 2
    assert q.hip_length == 4


def test_parameter_definitions():
    ids = {definition.parameter_id for definition in roof_parameter_definitions()}
    assert {"pitch_degrees", "overhang", "projected_area", "sloped_area", "volume"} <= ids


def test_events():
    events = []
    engine = IntelligentRoofEngine(event_dispatcher=lambda name, payload: events.append((name, payload)))
    structure = RoofStructure((RoofLayer("core", "Core", RoofLayerFunction.STRUCTURE, 0.2),))
    engine.register_type(RoofType("t", "Type", structure))
    engine.add_roof(IntelligentRoof("r", "t", rect(4, 3)))
    assert events[0][0] == "roof.type.registered"
    assert events[-1][0] == "roof.added"


@pytest.mark.parametrize("index", range(17))
def test_additional_roof_catalog_cases(index):
    catalog = RoofTypeCatalog()
    structure = RoofStructure((
        RoofLayer("core", "Core", RoofLayerFunction.STRUCTURE, 0.20),
    ))
    roof_type = RoofType(f"extra-{index}", f"Extra {index}", structure)
    catalog.register(roof_type)
    assert catalog.get(roof_type.type_id) is roof_type
