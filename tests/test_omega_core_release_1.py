import pytest
from pathlib import Path
from aias_omega_core.commands import CommandBus
from aias_omega_core.events import EventBus, Event
from aias_omega_core.graph import ObjectGraph, Relationship
from aias_omega_core.ids import ObjectId
from aias_omega_core.materials import Material, MaterialLibrary
from aias_omega_core.objects import EngineeringObject
from aias_omega_core.persistence import ProjectSerializer
from aias_omega_core.plugins import PluginDescriptor, PluginRegistry
from aias_omega_core.project import EngineeringProject
from aias_omega_core.selection import SelectionService
from aias_omega_core.transactions import Transaction, TransactionManager
from aias_omega_core.units import UnitSystem
from aias_omega_core.workflows import create_cad_to_bim_to_structural_demo

@pytest.mark.parametrize("i", range(100))
def test_ids_objects(i):
    obj = EngineeringObject(object_type="cad_line", name=f"L{i}")
    old = obj.revision
    obj.set_property("x", i)
    assert obj.revision == old + 1
    assert ObjectId.parse(str(obj.object_id)) == obj.object_id

@pytest.mark.parametrize("i", range(100))
def test_graph(i):
    a, b = ObjectId.new(), ObjectId.new()
    graph = ObjectGraph()
    rel = Relationship(a, b, "connects")
    graph.add(rel)
    assert graph.outgoing(a) == (rel,)
    assert graph.incoming(b) == (rel,)

@pytest.mark.parametrize("i", range(100))
def test_events_commands(i):
    received = []
    bus = EventBus()
    bus.subscribe("x", lambda event: received.append(event.payload["i"]))
    bus.publish(Event("x", {"i": i}))
    assert received == [i]
    commands = CommandBus()
    commands.register("sum", lambda a, b: a + b)
    assert commands.execute("sum", i, 1).value == i + 1

@pytest.mark.parametrize("i", range(100))
def test_transactions_selection(i):
    value = {"x": 0}
    tx = Transaction(
        "set",
        undo_steps=[lambda: value.__setitem__("x", 0)],
        redo_steps=[lambda: value.__setitem__("x", 1)],
    )
    manager = TransactionManager()
    value["x"] = 1
    manager.commit(tx)
    assert manager.undo() and value["x"] == 0
    assert manager.redo() and value["x"] == 1
    selection = SelectionService()
    oid = ObjectId.new()
    selection.add(oid)
    assert selection.all() == (oid,)

@pytest.mark.parametrize("i", range(100))
def test_units_materials_plugins(i):
    units = UnitSystem()
    assert units.convert(1000, "mm", "m") == pytest.approx(1.0)
    library = MaterialLibrary()
    library.add(Material(f"M{i}", "Steel", "steel", {"E_MPa": 200000}))
    assert library.get(f"M{i}").category == "steel"
    plugins = PluginRegistry()
    plugins.register(PluginDescriptor(f"P{i}", "Demo", "1.0", lambda value: value + 1))
    assert plugins.create(f"P{i}", i) == i + 1

@pytest.mark.parametrize("i", range(100))
def test_project_persistence(tmp_path, i):
    project = EngineeringProject(f"P{i}")
    obj = EngineeringObject(object_type="bim_wall", name="W")
    project.add_object(obj)
    path = tmp_path / f"p{i}.json"
    ProjectSerializer().save(project, path)
    restored = ProjectSerializer().load(path)
    assert restored.name == f"P{i}"
    assert len(restored.objects) == 1

@pytest.mark.parametrize("i", range(100))
def test_cross_studio_workflow(i):
    project = create_cad_to_bim_to_structural_demo()
    assert {obj.object_type for obj in project.objects.values()} == {
        "cad_line", "bim_wall", "structural_member", "quantity_item"
    }
    assert len(project.graph.all()) == 3
