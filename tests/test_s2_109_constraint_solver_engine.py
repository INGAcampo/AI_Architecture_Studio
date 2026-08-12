import pytest

from engines.ai.constraints import (
    ConstraintSolver,
    ConstraintSystem,
    ConstraintVariable,
    DistanceConstraint,
    EqualityConstraint,
    FixedValueConstraint,
    MaximumConstraint,
    MinimumConstraint,
    SolverOptions,
)


@pytest.mark.parametrize("index", range(20))
def test_constraint_variables(index):
    variable = ConstraintVariable(f"v{index}", 12, minimum=0, maximum=10)
    assert variable.value == 10
    variable.value = -5
    variable.clamp()
    assert variable.value == 0


@pytest.mark.parametrize("index", range(20))
def test_fixed_and_equality_constraints(index):
    system = ConstraintSystem()
    system.add_variable(ConstraintVariable("a", index))
    system.add_variable(ConstraintVariable("b", index + 10))
    system.add_constraint(FixedValueConstraint("fix", "a", 5))
    system.add_constraint(EqualityConstraint("equal", "a", "b"))

    result = ConstraintSolver().solve(system)
    assert result.success
    assert result.values["a"] == pytest.approx(5)
    assert result.values["b"] == pytest.approx(5)


@pytest.mark.parametrize("index", range(20))
def test_minimum_and_maximum_constraints(index):
    system = ConstraintSystem()
    system.add_variable(ConstraintVariable("width", 0.50))
    system.add_variable(ConstraintVariable("height", 4.50))
    system.add_constraint(MinimumConstraint("min-width", "width", 0.80))
    system.add_constraint(MaximumConstraint("max-height", "height", 3.00))

    result = ConstraintSolver().solve(system)
    assert result.success
    assert result.values["width"] == pytest.approx(0.80)
    assert result.values["height"] == pytest.approx(3.00)


@pytest.mark.parametrize("index", range(20))
def test_distance_constraint(index):
    system = ConstraintSystem()
    system.add_variable(ConstraintVariable("ax", 0))
    system.add_variable(ConstraintVariable("ay", 0))
    system.add_variable(ConstraintVariable("bx", 3))
    system.add_variable(ConstraintVariable("by", 4))
    system.add_constraint(
        DistanceConstraint("distance", "ax", "ay", "bx", "by", 10)
    )

    result = ConstraintSolver().solve(system)
    assert result.success
    assert result.values["bx"] == pytest.approx(6)
    assert result.values["by"] == pytest.approx(8)


@pytest.mark.parametrize("index", range(20))
def test_validation(index):
    system = ConstraintSystem()
    system.add_variable(ConstraintVariable("x", 0))
    system.add_constraint(MinimumConstraint("min-x", "x", 5))

    violations = ConstraintSolver().validate(system)
    assert len(violations) == 1
    assert violations[0].constraint_id == "min-x"

    result = ConstraintSolver().solve(system)
    assert result.success
    assert ConstraintSolver().validate(system) == ()


@pytest.mark.parametrize("index", range(20))
def test_options_and_statistics(index):
    system = ConstraintSystem()
    system.add_variable(ConstraintVariable("x", 1))
    system.add_constraint(FixedValueConstraint("fix-x", "x", 2))

    result = ConstraintSolver().solve(
        system,
        options=SolverOptions(max_iterations=10, convergence_tolerance=1e-9),
    )
    assert result.success
    assert result.iterations >= 1
    assert result.values == {"x": 2.0}
