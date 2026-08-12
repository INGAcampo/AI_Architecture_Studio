import pytest

from engines.parametric.parameters import (
    ParameterAccess,
    ParameterDefinition,
    ParameterEngine,
    ParameterType,
)
from engines.parametric.formulas import (
    DependencyCycleError,
    FormulaDefinition,
    FormulaEngine,
    FormulaRepository,
    FormulaService,
    FormulaStatus,
    ParameterDependencyGraph,
    SafeFormulaParser,
)


@pytest.mark.parametrize("expression,expected", [
    ("1 + 2", 3),
    ("5 - 2", 3),
    ("3 * 4", 12),
    ("8 / 2", 4),
    ("2 ** 3", 8),
    ("10 % 3", 1),
    ("-5", -5),
    ("+5", 5),
    ("abs(-4)", 4),
    ("min(3, 7)", 3),
    ("max(3, 7)", 7),
    ("round(3.14159, 2)", 3.14),
    ("(2 + 3) * 4", 20),
    ("2 + 3 * 4", 14),
    ("100 / (5 * 4)", 5),
    ("2 ** 2 ** 2", 16),
    ("7 % 4 + 1", 4),
    ("abs(-2) + max(1, 3)", 5),
    ("min(5, 2) * 10", 20),
    ("round(2.675, 2)", 2.67),
])
def test_safe_parser_numeric_expressions(expression, expected):
    parser = SafeFormulaParser()
    parsed = parser.parse(expression)
    assert parser.evaluate(parsed, {}) == expected


@pytest.mark.parametrize("expression,dependencies", [
    ("length * height", ("height", "length")),
    ("area * thickness", ("area", "thickness")),
    ("a + b + c", ("a", "b", "c")),
    ("max(width, depth)", ("depth", "width")),
    ("abs(offset)", ("offset",)),
    ("round(volume, 2)", ("volume",)),
    ("x ** 2 + y ** 2", ("x", "y")),
    ("min(a, b) * h", ("a", "b", "h")),
    ("p1 + p2 - p3", ("p1", "p2", "p3")),
    ("value", ("value",)),
])
def test_dependency_extraction(expression, dependencies):
    parsed = SafeFormulaParser().parse(expression)
    assert parsed.dependencies == dependencies


@pytest.mark.parametrize("bad_expression", [
    "__import__('os')",
    "open('x')",
    "a.b",
    "[1, 2, 3]",
    "{'a': 1}",
    "lambda x: x",
    "x if y else z",
    "sum([1, 2])",
    "pow(2, 3)",
    "round(number=2.3)",
])
def test_unsafe_expressions_rejected(bad_expression):
    with pytest.raises(ValueError):
        SafeFormulaParser().parse(bad_expression)


@pytest.mark.parametrize("count", range(1, 11))
def test_graph_add_nodes(count):
    graph = ParameterDependencyGraph()
    for index in range(count):
        graph.add_node(f"n{index}")
    assert len(graph.topological_order()) == count


@pytest.mark.parametrize("count", range(2, 12))
def test_graph_linear_topological_order(count):
    graph = ParameterDependencyGraph()
    for index in range(count - 1):
        graph.add_dependency(f"n{index}", f"n{index + 1}")
    assert graph.topological_order() == tuple(f"n{index}" for index in range(count))


@pytest.mark.parametrize("count", range(2, 12))
def test_graph_transitive_dependents(count):
    graph = ParameterDependencyGraph()
    for index in range(count - 1):
        graph.add_dependency(f"n{index}", f"n{index + 1}")
    assert graph.transitive_dependents("n0") == tuple(f"n{index}" for index in range(1, count))


@pytest.mark.parametrize("index", range(10))
def test_repository_add_get_remove(index):
    repository = FormulaRepository()
    formula = FormulaDefinition(
        f"f{index}",
        "owner",
        f"target{index}",
        "1 + 1",
    )
    repository.add(formula)
    assert repository.get(formula.formula_id) is formula
    assert repository.remove(formula.formula_id) is formula


def make_parameter_engine():
    engine = ParameterEngine()
    engine.create_collection(
        "wall",
        [
            ParameterDefinition("length", "Length", ParameterType.LENGTH, default_value=5.0),
            ParameterDefinition("height", "Height", ParameterType.LENGTH, default_value=3.0),
            ParameterDefinition("thickness", "Thickness", ParameterType.LENGTH, default_value=0.2),
            ParameterDefinition("area", "Area", ParameterType.AREA, access=ParameterAccess.CALCULATED, default_value=0.0),
            ParameterDefinition("volume", "Volume", ParameterType.VOLUME, access=ParameterAccess.CALCULATED, default_value=0.0),
        ],
    )
    return engine


def test_formula_definition_validation():
    with pytest.raises(ValueError):
        FormulaDefinition("", "owner", "target", "1")
    with pytest.raises(ValueError):
        FormulaDefinition("f", "", "target", "1")
    with pytest.raises(ValueError):
        FormulaDefinition("f", "owner", "", "1")
    with pytest.raises(ValueError):
        FormulaDefinition("f", "owner", "target", "")


def test_graph_rejects_self_cycle():
    with pytest.raises(DependencyCycleError):
        ParameterDependencyGraph().add_dependency("a", "a")


def test_graph_rejects_indirect_cycle():
    graph = ParameterDependencyGraph()
    graph.add_dependency("a", "b")
    graph.add_dependency("b", "c")
    with pytest.raises(DependencyCycleError):
        graph.add_dependency("c", "a")


def test_formula_engine_evaluates_area():
    parameters = make_parameter_engine()
    formulas = FormulaEngine(parameters)
    formulas.add_formula(FormulaDefinition("area", "wall", "area", "length * height"))
    result = formulas.evaluate("area")
    assert result.success
    assert result.value == 15.0
    assert parameters.get_collection("wall").value("area") == 15.0


def test_formula_engine_evaluates_chain():
    parameters = make_parameter_engine()
    formulas = FormulaEngine(parameters)
    formulas.add_formula(FormulaDefinition("area", "wall", "area", "length * height"))
    formulas.add_formula(FormulaDefinition("volume", "wall", "volume", "area * thickness"))
    results = formulas.evaluate_owner("wall")
    assert [result.target_parameter for result in results] == ["area", "volume"]
    assert parameters.get_collection("wall").value("volume") == 3.0


def test_formula_propagation():
    parameters = make_parameter_engine()
    formulas = FormulaEngine(parameters)
    formulas.add_formula(FormulaDefinition("area", "wall", "area", "length * height"))
    formulas.add_formula(FormulaDefinition("volume", "wall", "volume", "area * thickness"))
    formulas.evaluate_owner("wall")
    parameters.set_value("wall", "height", 4.0)
    results = formulas.propagate("wall", "height")
    assert [result.target_parameter for result in results] == ["area", "volume"]
    assert parameters.get_collection("wall").value("volume") == 4.0


def test_disabled_formula():
    parameters = make_parameter_engine()
    formulas = FormulaEngine(parameters)
    formula = FormulaDefinition("area", "wall", "area", "length * height", enabled=False)
    formulas.add_formula(formula)
    result = formulas.evaluate("area")
    assert not result.success
    assert formula.status is FormulaStatus.DISABLED


def test_formula_missing_parameter_reports_error():
    parameters = make_parameter_engine()
    formulas = FormulaEngine(parameters)
    formulas.add_formula(FormulaDefinition("bad", "wall", "area", "missing * 2"))
    result = formulas.evaluate("bad")
    assert not result.success
    assert result.error


def test_formula_remove_updates_graph():
    parameters = make_parameter_engine()
    formulas = FormulaEngine(parameters)
    formulas.add_formula(FormulaDefinition("area", "wall", "area", "length * height"))
    formulas.remove_formula("area")
    assert formulas.graph.dependencies_of("wall:area") == ()


def test_formula_service():
    parameters = make_parameter_engine()
    engine = FormulaEngine(parameters)
    service = FormulaService(engine)
    service.define("area", "wall", "area", "length * height")
    assert service.recalculate("wall")[0].value == 15.0


def test_formula_events():
    events = []
    parameters = make_parameter_engine()
    engine = FormulaEngine(
        parameters,
        event_dispatcher=lambda name, payload: events.append((name, payload)),
    )
    engine.add_formula(FormulaDefinition("area", "wall", "area", "length * height"))
    engine.evaluate("area")
    assert events[0][0] == "formula.added"
    assert events[-1][0] == "formula.evaluated"


@pytest.mark.parametrize("index", range(20))
def test_formula_parameter_variations(index):
    parameters = ParameterEngine()
    parameters.create_collection(
        f"owner-{index}",
        [
            ParameterDefinition("a", "A", ParameterType.FLOAT, default_value=float(index)),
            ParameterDefinition("b", "B", ParameterType.FLOAT, default_value=2.0),
            ParameterDefinition("result", "Result", ParameterType.FLOAT, access=ParameterAccess.CALCULATED, default_value=0.0),
        ],
    )
    formulas = FormulaEngine(parameters)
    formulas.add_formula(
        FormulaDefinition(
            f"formula-{index}",
            f"owner-{index}",
            "result",
            "a * b + 1",
        )
    )
    result = formulas.evaluate(f"formula-{index}")
    assert result.value == float(index) * 2.0 + 1.0


@pytest.mark.parametrize("index", range(9))
def test_graph_remove_dependency_cases(index):
    graph = ParameterDependencyGraph()
    source = f"source-{index}"
    target = f"target-{index}"
    graph.add_dependency(source, target)
    assert graph.remove_dependency(source, target)
    assert graph.dependencies_of(target) == ()
    assert not graph.remove_dependency(source, target)
