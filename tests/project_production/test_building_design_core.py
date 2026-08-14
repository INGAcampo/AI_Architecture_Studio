from aias_building_design_core import BuildingDesignCore


def test_pilot_graph_seeds_and_persists(tmp_path):
    core = BuildingDesignCore()
    graph = core.seed_pilot(core.create_project("Pilot Building"))
    assert core.validate(graph) == []
    types = {node["type"] for node in graph.nodes}
    assert {"site", "level", "grid", "space", "wall", "door", "window", "slab", "foundation"} <= types
    path = tmp_path / "pilot.json"
    graph.save(path)
    loaded = graph.load(path)
    assert loaded.to_dict() == graph.to_dict()
