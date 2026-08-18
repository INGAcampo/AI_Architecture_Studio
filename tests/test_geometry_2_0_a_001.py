import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def test_occt_gate_is_explicitly_pending_without_blocking_aias_native_geometry():
    evidence = json.loads((ROOT / "engineering/aias/geometry/GEOMETRY_2_0_A_001_AVAILABILITY.json").read_text(encoding="utf-8"))
    assert evidence["available"] is False
    assert evidence["production_ready"] is False
    assert evidence["no_blocking_claim"] is True
