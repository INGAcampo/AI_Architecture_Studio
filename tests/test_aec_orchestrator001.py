import json
from pathlib import Path
import pytest
from aias_aec_orchestrator import WorkerContract, WorkerRegistry, WorkerState
ROOT=Path(__file__).resolve().parents[1]
def test_unlicensed_external_worker_fails_closed():
    registry=WorkerRegistry(); registry.register(WorkerContract("revit","Revit",("bim_query",)))
    assert registry.open("revit").state == WorkerState.UNAVAILABLE
def test_worker_registry_rejects_duplicates():
    registry=WorkerRegistry(); worker=WorkerContract("cad","AutoCAD",("dwg_import",)); registry.register(worker)
    with pytest.raises(ValueError,match="duplicate_worker"): registry.register(worker)
def test_worker_registry_declares_all_target_products():
    data=json.loads((ROOT/"engineering/aias/aec_orchestrator/WORKER_REGISTRY.json").read_text(encoding="utf-8"))
    assert {item["product"] for item in data["workers"]} == {"AutoCAD","Revit","ETABS","SAP2000","SAFE","GEO5"}
