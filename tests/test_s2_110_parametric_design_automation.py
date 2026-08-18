import pytest

from engines.ai.parametric_automation import (
    DependencyCycleError,
    DependencyGraph,
    Formula,
    FormulaError,
    ParameterDefinition,
    ParameterSet,
    ParameterType,
    ParametricAutomationEngine,
    RegenerationService,
)


@pytest.mark.parametrize("index", range(20))
def test_parameter_model(index):
    params = ParameterSet(f"owner-{index}")
    params.define(
        ParameterDefinition(
            "width",
            ParameterType.LENGTH,
            1.0,
            minimum=0.5,
            maximum=5.0,
        )
    )
    assert params.get("width") == 1.0
    assert params.set("width", 2.0)
    assert params.get("width") == 2.0
    assert params.revision == 1


@pytest.mark.parametrize("index", range(20))
def test_formula_engine(index):
    formula = Formula("area", "width * height")
    assert formula.dependencies() == ("height", "width")
    assert formula.evaluate({"width": 3, "height": 4}) == 12

    trig = Formula("rise", "length * sin(radians(angle))")
    result = trig.evaluate({"length": 10, "angle": 30})
    assert result == pytest.approx(5)


@pytest.mark.parametrize("index", range(20))
def test_dependency_graph(index):
    graph = DependencyGraph()
    graph.add_dependency("area", "width")
    graph.add_dependency("area", "height")
    graph.add_dependency("volume", "area")
    graph.add_dependency("volume", "depth")

    assert graph.dependencies_of("area") == ("height", "width")
    assert graph.affected_by("width") == ("area", "volume")

    with pytest.raises(DependencyCycleError):
        graph.add_dependency("width", "volume")


@pytest.mark.parametrize("index", range(20))
def test_regeneration(index):
    params = ParameterSet(f"wall-{index}")
    params.define(ParameterDefinition("width", ParameterType.LENGTH, 4.0))
    params.define(ParameterDefinition("height", ParameterType.LENGTH, 3.0))
    params.define(
        ParameterDefinition(
            "area",
            ParameterType.AREA,
            12.0,
            read_only=True,
        )
    )

    service = RegenerationService()
    service.register_formula(Formula("area", "width * height"))

    params.set("width", 5.0)
    report = service.regenerate(
        params,
        changed_parameter_ids=("width",),
    )

    assert report.success
    assert params.get("area") == 15.0
    assert report.changed_parameters == ("area",)


@pytest.mark.parametrize("index", range(20))
def test_automation_transaction(index):
    engine = ParametricAutomationEngine()
    engine.create_parameter_set(
        f"wall-{index}",
        (
            ParameterDefinition("width", ParameterType.LENGTH, 4.0),
            ParameterDefinition("height", ParameterType.LENGTH, 3.0),
            ParameterDefinition(
                "area",
                ParameterType.AREA,
                12.0,
                read_only=True,
            ),
            ParameterDefinition(
                "volume",
                ParameterType.VOLUME,
                2.4,
                read_only=True,
            ),
            ParameterDefinition("thickness", ParameterType.LENGTH, 0.2),
        ),
    )
    engine.register_formula(
        f"wall-{index}",
        Formula("area", "width * height"),
    )
    engine.register_formula(
        f"wall-{index}",
        Formula("volume", "area * thickness"),
    )

    result = engine.set_values(
        f"wall-{index}",
        {"width": 5.0, "height": 4.0},
    )

    assert result.success
    values = engine.parameters(f"wall-{index}").values()
    assert values["area"] == 20.0
    assert values["volume"] == 4.0


@pytest.mark.parametrize("index", range(20))
def test_transaction_rollback(index):
    engine = ParametricAutomationEngine()
    engine.create_parameter_set(
        f"door-{index}",
        (
            ParameterDefinition(
                "width",
                ParameterType.LENGTH,
                0.9,
                minimum=0.8,
            ),
            ParameterDefinition(
                "area",
                ParameterType.AREA,
                1.89,
                read_only=True,
            ),
            ParameterDefinition("height", ParameterType.LENGTH, 2.1),
        ),
    )
    engine.register_formula(
        f"door-{index}",
        Formula("area", "width * height"),
    )

    result = engine.set_values(
        f"door-{index}",
        {"width": 0.5},
    )

    assert not result.success
    assert engine.parameters(f"door-{index}").get("width") == 0.9
