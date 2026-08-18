from __future__ import annotations

from engines.bim import (
    BimElement,
    BimEventName,
    BimService,
    ProjectBimManager,
    RelationshipType,
)
from engines.geometry.point import Point
from kernel.event_bus import EventBus
from kernel.service_locator import ServiceLocator
from models.architectural.door import Door
from models.architectural.wall import Wall


def _wall() -> Wall:
    return Wall([Point(0, 0), Point(5, 0)], thickness=0.20, height=3.0)


def test_service_register_find_update_and_remove() -> None:
    service = BimService()
    wall = _wall()

    registered = service.register(wall)
    assert service.find(wall.id) is registered
    assert service.element_count == 1

    wall.thickness = 0.30
    updated = service.update(wall)
    assert updated is registered
    assert updated.parameters["Thickness"] == 0.30

    removed = service.remove(wall.id)
    assert removed.element_id == wall.id
    assert service.find(wall.id) is None
    assert service.element_count == 0


def test_duplicate_registration_becomes_idempotent_update() -> None:
    service = BimService()
    wall = _wall()

    first = service.register(wall)
    wall.height = 4.0
    second = service.register(wall)

    assert first is second
    assert service.element_count == 1
    assert second.parameters["Height"] == 4.0


def test_parameter_change_syncs_source_properties_and_emits_event() -> None:
    service = BimService()
    wall = _wall()
    wall.properties = {}
    element = service.register(wall)
    events = []
    service.events.subscribe(BimEventName.PARAMETER_CHANGED, events.append)

    previous = service.set_parameter(
        element.element_id,
        "FireRating",
        "120 min",
        group="Performance",
    )

    assert previous is None
    assert element.parameters["FireRating"] == "120 min"
    assert wall.properties["FireRating"] == "120 min"
    assert events[0].element_id == wall.id


def test_service_infers_host_relationship_and_avoids_duplicates() -> None:
    service = BimService()
    wall = _wall()

    class Opening:
        def __init__(self, host_wall):
            self.host_wall = host_wall
            self.center_point = Point(1, 0)

    door = Door(opening=Opening(wall), width=0.90)
    service.register(wall)
    door_element = service.register(door)
    service.update(door)

    relations = service.document.relationships_for(door_element.element_id)
    assert len(relations) == 1
    assert relations[0].relationship_type is RelationshipType.HOSTS
    assert relations[0].source_id == wall.id


def test_repository_round_trip_replaces_active_document(tmp_path) -> None:
    service = BimService()
    element = service.register(BimElement("Muro BIM", "Wall"))
    target = tmp_path / "model.bim.json"

    service.save(target)
    service.new_document("Vacío")
    assert service.element_count == 0

    restored = service.load(target)
    assert restored.name == "Proyecto BIM"
    assert service.require(element.element_id).name == "Muro BIM"


def test_external_event_bus_receives_bim_events() -> None:
    event_bus = EventBus()
    received = []
    event_bus.subscribe(BimEventName.ELEMENT_REGISTERED.value, received.append)
    service = BimService(event_bus=event_bus)

    service.register(BimElement("Nivel 1", "Storey"))

    assert received[0].name is BimEventName.ELEMENT_REGISTERED


def test_project_manager_registers_service_and_uses_default_path(tmp_path) -> None:
    locator = ServiceLocator()
    project_file = tmp_path / "Hotel.aias.json"
    manager = ProjectBimManager(
        project_path=project_file,
        service_locator=locator,
    )
    manager.service.register(BimElement("Proyecto", "Project"))

    saved = manager.save()

    assert locator.get("bim_service") is manager.service
    assert saved == tmp_path / "Hotel.aias.bim.json"
    assert saved.exists()
