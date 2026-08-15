from aias_building_design_core import BuildingDesignCore
from aias_building_design_core import NativeBimProjection


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

def test_native_bim_projection_is_derived_from_project_graph():
    from aias_project_intake.builders import ParametricProjectGraphBuilder
    manifest={'project_id':'BIM-001','project_name':'BIM','mode':'PILOT_SYNTHETIC','scenario_id':'NOMINAL_CASE_001','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True,'building_program':{'levels':2,'width_m':8,'length_m':9,'storey_height_m':3}}
    projection=NativeBimProjection().materialize(ParametricProjectGraphBuilder().build(manifest))
    assert len(projection['walls']) == 8
    assert projection['traceability']['source'] == 'ProjectGraph'
    assert all(not wall['issues'] for wall in projection['walls'].values())
