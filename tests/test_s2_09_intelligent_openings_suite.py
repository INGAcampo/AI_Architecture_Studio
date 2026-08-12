import pytest

from engines.bim.openings import (
    HostWallGeometry,
    IntelligentOpeningEngine,
    Opening,
    OpeningCollisionDetector,
    OpeningKind,
    OpeningPlacement,
    OpeningQuantityCalculator,
    OpeningRelationshipManager,
    OpeningState,
    OpeningValidator,
)


@pytest.mark.parametrize("kind", list(OpeningKind))
def test_opening_kinds(kind):
    opening = Opening("o", "w", kind, 1.0, 2.0, OpeningPlacement(0.5))
    assert opening.kind is kind


@pytest.mark.parametrize("width,height", [
    (0.7, 2.0), (0.8, 2.1), (0.9, 2.1), (1.0, 2.2), (1.2, 2.4),
    (1.5, 1.0), (1.8, 1.2), (2.0, 1.5), (2.4, 1.8), (3.0, 2.0),
])
def test_opening_area(width, height):
    opening = Opening("o", "w", OpeningKind.GENERIC, width, height, OpeningPlacement(0))
    assert opening.area == pytest.approx(width * height)


@pytest.mark.parametrize("offset,width,expected", [
    (0, 1, 0.5), (1, 1, 1.5), (2, 1, 2.5), (3, 2, 4.0), (4, 2, 5.0),
    (5, 3, 6.5), (0.5, 1.5, 1.25), (2.5, 0.5, 2.75), (6, 1, 6.5), (7, 0.8, 7.4),
])
def test_center_offset(offset, width, expected):
    opening = Opening("o", "w", OpeningKind.GENERIC, width, 1, OpeningPlacement(offset))
    assert opening.center_offset == pytest.approx(expected)


@pytest.mark.parametrize("sill,height,head", [
    (0, 2.1, 2.1), (0.9, 1.2, 2.1), (1.0, 1.0, 2.0), (0.5, 1.5, 2.0),
    (0.2, 2.0, 2.2), (1.2, 0.8, 2.0), (0.8, 1.4, 2.2), (0.0, 3.0, 3.0),
    (1.5, 0.5, 2.0), (0.75, 1.25, 2.0),
])
def test_head_height(sill, height, head):
    opening = Opening("o", "w", OpeningKind.WINDOW, 1, height, OpeningPlacement(0, sill))
    assert opening.head_height == pytest.approx(head)


@pytest.mark.parametrize("offset", [0, 0.1, 1, 2, 3, 4, 5, 6, 7, 8])
def test_validator_valid_offsets(offset):
    wall = HostWallGeometry("w", 10, 3, 0.2)
    opening = Opening("o", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(offset))
    assert OpeningValidator().validate(opening, wall).valid


@pytest.mark.parametrize("offset", [-1, -0.1, 9.1, 10, 11])
def test_validator_invalid_offsets(offset):
    wall = HostWallGeometry("w", 10, 3, 0.2)
    opening = Opening("o", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(offset))
    assert not OpeningValidator().validate(opening, wall).valid


@pytest.mark.parametrize("sill,height", [(2.5, 1), (2, 2), (3, 0.5), (-0.1, 1), (1.5, 2)])
def test_validator_invalid_vertical(sill, height):
    wall = HostWallGeometry("w", 10, 3, 0.2)
    opening = Opening("o", "w", OpeningKind.WINDOW, 1, height, OpeningPlacement(1, sill))
    assert not OpeningValidator().validate(opening, wall).valid


@pytest.mark.parametrize("count", range(1, 11))
def test_relationship_order(count):
    manager = OpeningRelationshipManager()
    for index in reversed(range(count)):
        manager.attach(
            Opening(
                f"o{index}",
                "w",
                OpeningKind.GENERIC,
                0.5,
                1,
                OpeningPlacement(float(index)),
            )
        )
    assert [o.opening_id for o in manager.for_wall("w")] == [f"o{i}" for i in range(count)]


@pytest.mark.parametrize("count", range(1, 11))
def test_quantity_calculation(count):
    wall = HostWallGeometry("w", 10, 3, 0.2)
    openings = tuple(
        Opening(
            f"o{i}",
            "w",
            OpeningKind.GENERIC,
            0.5,
            1,
            OpeningPlacement(i),
        )
        for i in range(count)
    )
    q = OpeningQuantityCalculator().calculate(wall, openings)
    assert q.opening_area == pytest.approx(count * 0.5)
    assert q.net_area == pytest.approx(30 - count * 0.5)


@pytest.mark.parametrize("distance", [0.1, 0.2, 0.5, 0.9])
def test_collision_detected(distance):
    first = Opening("a", "w", OpeningKind.GENERIC, 1, 1, OpeningPlacement(0, 0))
    second = Opening("b", "w", OpeningKind.GENERIC, 1, 1, OpeningPlacement(distance, 0))
    assert OpeningCollisionDetector().detect((first, second))


@pytest.mark.parametrize("distance", [1.0, 1.1, 2.0, 5.0, 10.0])
def test_collision_not_detected(distance):
    first = Opening("a", "w", OpeningKind.GENERIC, 1, 1, OpeningPlacement(0, 0))
    second = Opening("b", "w", OpeningKind.GENERIC, 1, 1, OpeningPlacement(distance, 0))
    assert not OpeningCollisionDetector().detect((first, second))


def make_engine():
    engine = IntelligentOpeningEngine()
    engine.register_wall(HostWallGeometry("w", 10, 3, 0.2))
    return engine


def test_model_validation():
    with pytest.raises(ValueError):
        Opening("", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(0))
    with pytest.raises(ValueError):
        Opening("o", "", OpeningKind.DOOR, 1, 2, OpeningPlacement(0))
    with pytest.raises(ValueError):
        Opening("o", "w", OpeningKind.DOOR, 0, 2, OpeningPlacement(0))


def test_engine_add_remove():
    engine = make_engine()
    opening = Opening("o", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(1))
    engine.add_opening(opening)
    assert engine.remove_opening("o") is opening


def test_engine_rejects_collision():
    engine = make_engine()
    engine.add_opening(Opening("a", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(1)))
    with pytest.raises(ValueError):
        engine.add_opening(Opening("b", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(1.5)))


def test_engine_resize():
    engine = make_engine()
    engine.add_opening(Opening("o", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(1)))
    engine.resize("o", 1.2, 2.1)
    assert engine.relationships.get("o").width == 1.2


def test_engine_resize_rolls_back_on_error():
    engine = make_engine()
    engine.add_opening(Opening("o", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(9)))
    with pytest.raises(ValueError):
        engine.resize("o", 2, 2)
    assert engine.relationships.get("o").width == 1


def test_engine_move():
    engine = make_engine()
    engine.add_opening(Opening("o", "w", OpeningKind.WINDOW, 1, 1, OpeningPlacement(1, 1)))
    engine.move("o", offset=2, sill_height=0.8)
    assert engine.relationships.get("o").placement == OpeningPlacement(2, 0.8)


def test_engine_suppress():
    engine = make_engine()
    engine.add_opening(Opening("o", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(1)))
    engine.suppress("o")
    assert engine.relationships.get("o").state is OpeningState.SUPPRESSED


def test_wall_quantities_ignore_suppressed():
    engine = make_engine()
    engine.add_opening(Opening("o", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(1)))
    engine.suppress("o")
    assert engine.wall_quantities("w").opening_area == 0


def test_wall_update_preserves_relative_position():
    engine = make_engine()
    engine.add_opening(Opening("o", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(2)))
    engine.update_wall(HostWallGeometry("w", 20, 3, 0.2))
    assert engine.relationships.get("o").placement.offset == pytest.approx(4)


def test_events():
    events = []
    engine = IntelligentOpeningEngine(event_dispatcher=lambda name, payload: events.append((name, payload)))
    engine.register_wall(HostWallGeometry("w", 10, 3, 0.2))
    engine.add_opening(Opening("o", "w", OpeningKind.DOOR, 1, 2, OpeningPlacement(1)))
    assert events[0][0] == "opening.wall.registered"
    assert events[-1][0] == "opening.added"


@pytest.mark.parametrize("index", range(12))
def test_engine_many_independent_openings(index):
    engine = IntelligentOpeningEngine()
    wall_id = f"w{index}"
    engine.register_wall(HostWallGeometry(wall_id, 10, 3, 0.2))
    opening = Opening(f"o{index}", wall_id, OpeningKind.WINDOW, 1, 1, OpeningPlacement(1, 1))
    engine.add_opening(opening)
    assert engine.relationships.get(opening.opening_id) is opening


@pytest.mark.parametrize("index", range(16))
def test_relationship_attach_detach_cases(index):
    manager = OpeningRelationshipManager()
    opening = Opening(
        f"detach-{index}",
        f"wall-{index}",
        OpeningKind.GENERIC,
        1.0,
        1.0,
        OpeningPlacement(0.0),
    )
    manager.attach(opening)
    assert manager.get(opening.opening_id) is opening
    assert manager.detach(opening.opening_id) is opening
    assert manager.for_wall(opening.host_wall_id) == ()
