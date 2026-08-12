import pytest

from engines.parametric.constraints import (
    ConstraintConflictDetector,
    ConstraintDefinition,
    ConstraintEvaluator,
    ConstraintGeometryStore,
    ConstraintKind,
    ConstraintPoint,
    ConstraintRepository,
    ConstraintSegment,
    ConstraintService,
    ConstraintSolver,
    ConstraintStatus,
    ConstraintTarget,
    equal_length,
    horizontal,
    parallel,
    perpendicular,
    point_distance,
    points_close,
    vertical,
)


@pytest.mark.parametrize("x,y,z", [(i, i + 1, 0.0) for i in range(20)])
def test_point_creation(x, y, z):
    point = ConstraintPoint(x, y, z)
    assert point.x == x
    assert point.y == y


@pytest.mark.parametrize("dx,dy", [(i, -i) for i in range(10)])
def test_point_moved(dx, dy):
    point = ConstraintPoint(1, 2).moved(dx, dy)
    assert point == ConstraintPoint(1 + dx, 2 + dy)


@pytest.mark.parametrize("end", [
    ConstraintPoint(1, 0), ConstraintPoint(2, 0), ConstraintPoint(3, 0),
    ConstraintPoint(4, 0), ConstraintPoint(5, 0), ConstraintPoint(-1, 0),
    ConstraintPoint(-2, 0), ConstraintPoint(0.5, 0), ConstraintPoint(10, 0),
    ConstraintPoint(100, 0),
])
def test_horizontal_segments(end):
    assert horizontal(ConstraintSegment(ConstraintPoint(0, 0), end))


@pytest.mark.parametrize("end", [
    ConstraintPoint(0, 1), ConstraintPoint(0, 2), ConstraintPoint(0, 3),
    ConstraintPoint(0, 4), ConstraintPoint(0, 5), ConstraintPoint(0, -1),
    ConstraintPoint(0, -2), ConstraintPoint(0, 0.5), ConstraintPoint(0, 10),
    ConstraintPoint(0, 100),
])
def test_vertical_segments(end):
    assert vertical(ConstraintSegment(ConstraintPoint(0, 0), end))


@pytest.mark.parametrize("scale", range(1, 11))
def test_parallel_segments(scale):
    a = ConstraintSegment(ConstraintPoint(0, 0), ConstraintPoint(1, 1))
    b = ConstraintSegment(ConstraintPoint(0, 2), ConstraintPoint(scale, 2 + scale))
    assert parallel(a, b)


@pytest.mark.parametrize("scale", range(1, 11))
def test_perpendicular_segments(scale):
    a = ConstraintSegment(ConstraintPoint(0, 0), ConstraintPoint(1, 0))
    b = ConstraintSegment(ConstraintPoint(0, 0), ConstraintPoint(0, scale))
    assert perpendicular(a, b)


@pytest.mark.parametrize("length", range(1, 11))
def test_equal_length_segments(length):
    a = ConstraintSegment(ConstraintPoint(0, 0), ConstraintPoint(length, 0))
    b = ConstraintSegment(ConstraintPoint(0, 0), ConstraintPoint(0, length))
    assert equal_length(a, b)


@pytest.mark.parametrize("distance", range(1, 11))
def test_point_distance(distance):
    assert point_distance(ConstraintPoint(0, 0), ConstraintPoint(distance, 0)) == distance


@pytest.mark.parametrize("kind", list(ConstraintKind))
def test_constraint_definition_kinds(kind):
    definition = ConstraintDefinition(
        f"c.{kind.value}",
        kind,
        (ConstraintTarget("obj", "geometry"),),
        value=1.0 if kind in {ConstraintKind.DISTANCE, ConstraintKind.OFFSET} else None,
    )
    assert definition.kind is kind


def make_store():
    store = ConstraintGeometryStore()
    store.set_element("a", "segment", ConstraintSegment(ConstraintPoint(0, 0), ConstraintPoint(2, 0)))
    store.set_element("b", "segment", ConstraintSegment(ConstraintPoint(0, 0), ConstraintPoint(0, 2)))
    store.set_element("a", "point", ConstraintPoint(0, 0))
    store.set_element("b", "point", ConstraintPoint(0, 0))
    store.set_element("c", "point", ConstraintPoint(3, 0))
    return store


def test_store_revision_only_changes_on_real_change():
    store = ConstraintGeometryStore()
    point = ConstraintPoint(0, 0)
    store.set_element("a", "p", point)
    store.set_element("a", "p", point)
    assert store.revision == 1


def test_repository_priority_order():
    repository = ConstraintRepository()
    repository.add(ConstraintDefinition("b", ConstraintKind.HORIZONTAL, (ConstraintTarget("o", "s"),), priority=20))
    repository.add(ConstraintDefinition("a", ConstraintKind.HORIZONTAL, (ConstraintTarget("o", "s"),), priority=10))
    assert [c.constraint_id for c in repository.all()] == ["a", "b"]


def test_evaluate_horizontal():
    store = make_store()
    evaluator = ConstraintEvaluator(store)
    c = ConstraintDefinition("c", ConstraintKind.HORIZONTAL, (ConstraintTarget("a", "segment"),))
    assert evaluator.evaluate(c).status is ConstraintStatus.SATISFIED


def test_evaluate_vertical():
    store = make_store()
    evaluator = ConstraintEvaluator(store)
    c = ConstraintDefinition("c", ConstraintKind.VERTICAL, (ConstraintTarget("b", "segment"),))
    assert evaluator.evaluate(c).satisfied


def test_evaluate_parallel():
    store = make_store()
    store.set_element("d", "segment", ConstraintSegment(ConstraintPoint(1, 1), ConstraintPoint(3, 1)))
    c = ConstraintDefinition("c", ConstraintKind.PARALLEL, (
        ConstraintTarget("a", "segment"),
        ConstraintTarget("d", "segment"),
    ))
    assert ConstraintEvaluator(store).evaluate(c).satisfied


def test_evaluate_perpendicular():
    store = make_store()
    c = ConstraintDefinition("c", ConstraintKind.PERPENDICULAR, (
        ConstraintTarget("a", "segment"),
        ConstraintTarget("b", "segment"),
    ))
    assert ConstraintEvaluator(store).evaluate(c).satisfied


def test_evaluate_coincident():
    store = make_store()
    c = ConstraintDefinition("c", ConstraintKind.COINCIDENT, (
        ConstraintTarget("a", "point"),
        ConstraintTarget("b", "point"),
    ))
    assert ConstraintEvaluator(store).evaluate(c).satisfied


def test_evaluate_equal_length():
    store = make_store()
    c = ConstraintDefinition("c", ConstraintKind.EQUAL_LENGTH, (
        ConstraintTarget("a", "segment"),
        ConstraintTarget("b", "segment"),
    ))
    assert ConstraintEvaluator(store).evaluate(c).satisfied


def test_evaluate_distance():
    store = make_store()
    c = ConstraintDefinition("c", ConstraintKind.DISTANCE, (
        ConstraintTarget("a", "point"),
        ConstraintTarget("c", "point"),
    ), value=3.0)
    assert ConstraintEvaluator(store).evaluate(c).satisfied


def test_evaluate_disabled():
    store = make_store()
    c = ConstraintDefinition("c", ConstraintKind.HORIZONTAL, (ConstraintTarget("a", "segment"),), enabled=False)
    assert ConstraintEvaluator(store).evaluate(c).status is ConstraintStatus.DISABLED


def test_evaluate_missing_geometry_conflict():
    store = make_store()
    c = ConstraintDefinition("c", ConstraintKind.HORIZONTAL, (ConstraintTarget("x", "segment"),))
    assert ConstraintEvaluator(store).evaluate(c).status is ConstraintStatus.CONFLICT


def test_horizontal_vertical_conflict():
    target = (ConstraintTarget("a", "segment"),)
    constraints = (
        ConstraintDefinition("h", ConstraintKind.HORIZONTAL, target),
        ConstraintDefinition("v", ConstraintKind.VERTICAL, target),
    )
    conflicts = ConstraintConflictDetector().detect(constraints)
    assert len(conflicts) == 1


def test_parallel_perpendicular_conflict():
    targets = (ConstraintTarget("a", "segment"), ConstraintTarget("b", "segment"))
    constraints = (
        ConstraintDefinition("p", ConstraintKind.PARALLEL, targets),
        ConstraintDefinition("q", ConstraintKind.PERPENDICULAR, targets),
    )
    assert ConstraintConflictDetector().detect(constraints)


def test_distance_conflict():
    targets = (ConstraintTarget("a", "point"), ConstraintTarget("b", "point"))
    constraints = (
        ConstraintDefinition("d1", ConstraintKind.DISTANCE, targets, value=1),
        ConstraintDefinition("d2", ConstraintKind.DISTANCE, targets, value=2),
    )
    assert ConstraintConflictDetector().detect(constraints)


def test_solver_success():
    store = make_store()
    repo = ConstraintRepository()
    repo.add(ConstraintDefinition("h", ConstraintKind.HORIZONTAL, (ConstraintTarget("a", "segment"),)))
    report = ConstraintSolver(repo, ConstraintEvaluator(store)).solve()
    assert report.success


def test_solver_reports_violation():
    store = make_store()
    repo = ConstraintRepository()
    repo.add(ConstraintDefinition("v", ConstraintKind.VERTICAL, (ConstraintTarget("a", "segment"),)))
    report = ConstraintSolver(repo, ConstraintEvaluator(store)).solve()
    assert report.violated_count == 1


def test_solver_reports_conflict():
    store = make_store()
    repo = ConstraintRepository()
    target = (ConstraintTarget("a", "segment"),)
    repo.add(ConstraintDefinition("h", ConstraintKind.HORIZONTAL, target))
    repo.add(ConstraintDefinition("v", ConstraintKind.VERTICAL, target))
    report = ConstraintSolver(repo, ConstraintEvaluator(store)).solve()
    assert report.conflict_count == 1


def test_service_events():
    events = []
    service = ConstraintService(event_dispatcher=lambda name, payload: events.append((name, payload)))
    service.geometry.set_element("a", "segment", ConstraintSegment(ConstraintPoint(0, 0), ConstraintPoint(1, 0)))
    service.add_constraint(ConstraintDefinition("h", ConstraintKind.HORIZONTAL, (ConstraintTarget("a", "segment"),)))
    service.evaluate("h")
    service.solve()
    assert events[0][0] == "constraint.added"
    assert events[-1][0] == "constraint.solve.completed"


@pytest.mark.parametrize("index", range(3))
def test_repository_add_remove_cases(index):
    repo = ConstraintRepository()
    constraint = ConstraintDefinition(
        f"c{index}",
        ConstraintKind.HORIZONTAL,
        (ConstraintTarget(f"o{index}", "segment"),),
    )
    repo.add(constraint)
    assert repo.get(constraint.constraint_id) is constraint
    assert repo.remove(constraint.constraint_id) is constraint
