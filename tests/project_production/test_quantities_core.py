from aias_building_design_core import BuildingDesignCore
from aias_quantities_core import QuantityTakeoffEngine


def test_takeoff_boq_summary_and_csv(tmp_path):
    graph = BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot Building"))
    engine = QuantityTakeoffEngine(); package = engine.build(graph, {"concrete": 0.05})
    assert package.items and engine.summary(package)["slab"] > 0
    assert len(engine.evidence_sha256(package)) == 64
    path = tmp_path / "boq.csv"; engine.export_csv(package, path); assert "element_id" in path.read_text(encoding="utf-8")


def test_takeoff_rejects_negative_waste():
    graph = BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot Building"))
    try: QuantityTakeoffEngine().build(graph, {"concrete": -0.1})
    except ValueError: return
    raise AssertionError("negative waste factor was accepted")
