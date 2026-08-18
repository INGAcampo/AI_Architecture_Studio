import json
from pathlib import Path
from aias_geometry_bim_bridge import BridgeRecord, GeometryBimBridge
ROOT=Path(__file__).resolve().parents[1]
def test_fixture_round_trip_preserves_identity_and_geometry():
    payload=json.loads((ROOT/"tests/fixtures/geometry_bim/wall_record.json").read_text(encoding="utf-8")); geometry=payload["geometry"]
    result=GeometryBimBridge().round_trip(BridgeRecord(payload["object_id"],payload["ifc_class"],geometry["kind"],geometry["parameters"]))
    assert result == {"stable_identity":True,"same_ifc_class":True,"same_geometry":True}
def test_bridge_rejects_invalid_identity():
    try: GeometryBimBridge().export_record(BridgeRecord("","IfcWall","solid",{}))
    except ValueError as exc: assert str(exc) == "object_id cannot be empty"
    else: raise AssertionError("invalid identity accepted")
