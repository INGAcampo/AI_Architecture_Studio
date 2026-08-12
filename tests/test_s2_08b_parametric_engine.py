import pytest

from engines.parametric.parameters import (
    ParameterAccess,
    ParameterCollection,
    ParameterDefinition,
    ParameterDefinitionRegistry,
    ParameterEditAction,
    ParameterEngine,
    ParameterScope,
    ParameterSerializer,
    ParameterService,
    ParameterType,
    ParameterValidator,
    UnitDefinition,
    UnitRegistry,
    wall_parameter_schema,
)


@pytest.mark.parametrize("parameter_type", list(ParameterType))
def test_definition_supports_parameter_types(parameter_type):
    kwargs = {}
    if parameter_type is ParameterType.ENUM:
        kwargs["enum_values"] = ("A", "B")
        kwargs["default_value"] = "A"
    definition = ParameterDefinition(
        f"p.{parameter_type.value}",
        parameter_type.value,
        parameter_type,
        **kwargs,
    )
    assert definition.parameter_type is parameter_type


@pytest.mark.parametrize("scope", list(ParameterScope))
def test_definition_supports_scopes(scope):
    kwargs = {"shared_key": "shared.test"} if scope is ParameterScope.SHARED else {}
    definition = ParameterDefinition(
        f"scope.{scope.value}",
        "Scope",
        ParameterType.STRING,
        scope=scope,
        **kwargs,
    )
    assert definition.scope is scope


@pytest.mark.parametrize("value,expected", [
    ("true", True), ("1", True), ("yes", True), ("si", True), ("sí", True),
    ("false", False), ("0", False), ("no", False),
])
def test_boolean_normalization(value, expected):
    definition = ParameterDefinition("visible", "Visible", ParameterType.BOOLEAN)
    assert ParameterValidator().normalize(definition, value) is expected


@pytest.mark.parametrize("value", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_integer_normalization(value):
    definition = ParameterDefinition("count", "Count", ParameterType.INTEGER)
    assert ParameterValidator().normalize(definition, str(value)) == value


@pytest.mark.parametrize("value", [0.1, 0.2, 0.5, 1.0, 2.5, 3.0, 4.2, 10.0, 25.5, 100.0])
def test_float_normalization(value):
    definition = ParameterDefinition("height", "Height", ParameterType.LENGTH, unit="m")
    assert ParameterValidator().normalize(definition, str(value)) == value


@pytest.mark.parametrize("from_unit,to_unit,value,expected", [
    ("m", "cm", 1, 100),
    ("m", "mm", 1, 1000),
    ("cm", "m", 100, 1),
    ("mm", "m", 1000, 1),
    ("ft", "in", 1, 12),
    ("in", "ft", 12, 1),
    ("m³", "L", 1, 1000),
    ("L", "m³", 1000, 1),
    ("rad", "deg", 1, 57.29577951308232),
    ("deg", "rad", 57.29577951308232, 1),
])
def test_unit_conversion(from_unit, to_unit, value, expected):
    assert UnitRegistry().convert(value, from_unit, to_unit) == pytest.approx(expected)


@pytest.mark.parametrize("index", range(10))
def test_registry_register_get_remove(index):
    registry = ParameterDefinitionRegistry()
    definition = ParameterDefinition(
        f"p{index}",
        f"Parameter {index}",
        ParameterType.STRING,
    )
    registry.register(definition)
    assert registry.get(definition.parameter_id) is definition
    assert registry.remove(definition.parameter_id) is definition


@pytest.mark.parametrize("height", [2.4, 2.7, 3.0, 3.3, 3.6, 4.0, 4.5, 5.0, 6.0, 10.0])
def test_collection_set_height(height):
    collection = ParameterCollection("wall")
    definition = ParameterDefinition(
        "height",
        "Altura",
        ParameterType.LENGTH,
        unit="m",
        minimum=0.1,
        default_value=3.0,
    )
    collection.add_definition(definition)
    collection.set("height", height)
    assert collection.value("height") == height


@pytest.mark.parametrize("phase", ["Existing", "Demolition", "New Construction", "Future"])
def test_enum_values(phase):
    definition = ParameterDefinition(
        "phase",
        "Fase",
        ParameterType.ENUM,
        enum_values=("Existing", "Demolition", "New Construction", "Future"),
        default_value="New Construction",
    )
    collection = ParameterCollection("wall")
    collection.add_definition(definition)
    collection.set("phase", phase)
    assert collection.value("phase") == phase


@pytest.mark.parametrize("index", range(10))
def test_engine_collections(index):
    engine = ParameterEngine()
    collection = engine.create_collection(
        f"owner-{index}",
        [ParameterDefinition("name", "Nombre", ParameterType.STRING, default_value="X")],
    )
    assert engine.get_collection(f"owner-{index}") is collection


@pytest.mark.parametrize("index", range(10))
def test_serializer_roundtrip(index):
    registry = ParameterDefinitionRegistry()
    definition = ParameterDefinition(
        "value",
        "Valor",
        ParameterType.FLOAT,
        default_value=float(index),
    )
    registry.register(definition)
    collection = ParameterCollection(f"owner-{index}")
    collection.add_definition(definition)
    text = ParameterSerializer().dumps(collection)
    restored = ParameterSerializer().loads(text, registry)
    assert restored.snapshot() == collection.snapshot()


def test_definition_validation():
    with pytest.raises(ValueError):
        ParameterDefinition("", "Name", ParameterType.STRING)
    with pytest.raises(ValueError):
        ParameterDefinition("x", "", ParameterType.STRING)
    with pytest.raises(ValueError):
        ParameterDefinition("e", "Enum", ParameterType.ENUM)
    with pytest.raises(ValueError):
        ParameterDefinition("s", "Shared", ParameterType.STRING, scope=ParameterScope.SHARED)


def test_registry_duplicate_rejected():
    registry = ParameterDefinitionRegistry()
    definition = ParameterDefinition("x", "X", ParameterType.STRING)
    registry.register(definition)
    with pytest.raises(KeyError):
        registry.register(definition)


def test_collection_duplicate_rejected():
    collection = ParameterCollection("owner")
    definition = ParameterDefinition("x", "X", ParameterType.STRING)
    collection.add_definition(definition)
    with pytest.raises(KeyError):
        collection.add_definition(definition)


def test_read_only_rejected():
    collection = ParameterCollection("owner")
    definition = ParameterDefinition(
        "area",
        "Area",
        ParameterType.AREA,
        access=ParameterAccess.READ_ONLY,
        default_value=0.0,
    )
    collection.add_definition(definition)
    with pytest.raises(PermissionError):
        collection.set("area", 10)


def test_calculated_update_allowed():
    collection = ParameterCollection("owner")
    definition = ParameterDefinition(
        "area",
        "Area",
        ParameterType.AREA,
        access=ParameterAccess.CALCULATED,
        default_value=0.0,
    )
    collection.add_definition(definition)
    collection.set_calculated("area", 10)
    assert collection.value("area") == 10.0


def test_range_validation():
    definition = ParameterDefinition(
        "height",
        "Height",
        ParameterType.LENGTH,
        minimum=1.0,
        maximum=5.0,
        default_value=3.0,
    )
    collection = ParameterCollection("owner")
    collection.add_definition(definition)
    with pytest.raises(ValueError):
        collection.set("height", 0.5)


def test_engine_change_event():
    events = []
    engine = ParameterEngine(event_dispatcher=lambda name, payload: events.append((name, payload)))
    engine.create_collection(
        "wall",
        [ParameterDefinition("height", "Height", ParameterType.FLOAT, default_value=3.0)],
    )
    change = engine.set_value("wall", "height", 4.0)
    assert change.old_value == 3.0
    assert events[-1][0] == "parameter.changed"


def test_engine_no_change_returns_none():
    engine = ParameterEngine()
    engine.create_collection(
        "wall",
        [ParameterDefinition("height", "Height", ParameterType.FLOAT, default_value=3.0)],
    )
    assert engine.set_value("wall", "height", 3.0) is None


def test_history_action_undo_redo():
    engine = ParameterEngine()
    engine.create_collection(
        "wall",
        [ParameterDefinition("height", "Height", ParameterType.FLOAT, default_value=3.0)],
    )
    action = ParameterEditAction(engine, "wall", "height", 3.0, 4.0)
    action.redo()
    assert engine.get_collection("wall").value("height") == 4.0
    action.undo()
    assert engine.get_collection("wall").value("height") == 3.0


def test_service_uses_history():
    class History:
        def __init__(self):
            self.action = None
        def execute(self, action):
            self.action = action
            action.redo()

    engine = ParameterEngine()
    service = ParameterService(engine, history_manager=History())
    service.create_owner(
        "wall",
        [ParameterDefinition("height", "Height", ParameterType.FLOAT, default_value=3.0)],
    )
    action = service.edit("wall", "height", 4.0)
    assert action.new_value == 4.0


def test_wall_schema():
    schema = wall_parameter_schema()
    ids = {definition.parameter_id for definition in schema}
    assert {"height", "thickness", "area", "volume", "phase"} <= ids


@pytest.mark.parametrize("index", range(13))
def test_unit_registry_custom_units(index):
    registry = UnitRegistry()
    symbol = f"u{index}"
    registry.register(UnitDefinition(symbol, "custom", float(index + 1)))
    assert registry.get(symbol).to_si == float(index + 1)
