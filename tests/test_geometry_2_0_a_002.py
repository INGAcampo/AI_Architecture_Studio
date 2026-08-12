import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_occt_poc_fails_closed_and_preserves_native_fallback():
    poc=json.loads((ROOT/"engineering/aias/geometry/GEOMETRY_2_0_A_002_POC.json").read_text(encoding="utf-8"))
    assert poc["available"] is False and poc["production_ready"] is False
    assert poc["native_fallback"] == "aias_geometry_kernel"
    assert poc["import_succeeded"] is False
