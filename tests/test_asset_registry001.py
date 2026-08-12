import pytest
from aias_asset_registry import AssetRegistry,AssetRegistryError
from aias_asset_registry.bootstrap import ingest_master_inventory
def asset():return {"id":"CAP-000001","title":"Capability","asset_type":"CAPABILITY","version":"1.0.0","status":"PROPOSED","owner":"ENGINEERING_OFFICE","purpose":"Test","scope":"AIAS","source":"src/demo","requirements":["REQ-1"],"evidence":[],"dependencies":[],"legal_status":"REFERENCE_ONLY"}
def test_register_persists_and_queries(tmp_path):
 r=AssetRegistry(tmp_path/"registry.json");r.register(asset());assert AssetRegistry(tmp_path/"registry.json").query("CAPABILITY")[0]["id"]=="CAP-000001"
def test_duplicate_rejected(tmp_path):
 r=AssetRegistry(tmp_path/"r.json");r.register(asset())
 with pytest.raises(AssetRegistryError):r.register(asset())
def test_lifecycle_is_sequential_and_audited(tmp_path):
 r=AssetRegistry(tmp_path/"r.json");r.register(asset());r.transition("CAP-000001","SPECIFIED","tester","approved spec");assert len(r.data["events"])==2
 with pytest.raises(AssetRegistryError):r.transition("CAP-000001","RELEASED","tester","skip")
def test_unknown_dependency_rejected(tmp_path):
 r=AssetRegistry(tmp_path/"r.json");a=asset();a["dependencies"]=["MISSING-1"]
 with pytest.raises(AssetRegistryError):r.register(a)
def test_master_inventory_is_an_immediate_consumer(tmp_path):
 root=__import__("pathlib").Path(__file__).resolve().parents[1]
 inventory=root/"engineering/aias/master/inventory/AIAS_MASTER_CONCEPT_INVENTORY.json"
 result=ingest_master_inventory(inventory,tmp_path/"assets.json")
 expected=len(__import__("json").loads(inventory.read_text(encoding="utf-8"))["concepts"])
 assert result["ingested"]==expected

