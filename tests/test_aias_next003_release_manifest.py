import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_release_manifest_artifacts_exist():
    manifest=json.loads((ROOT/"engineering/aias/release_gate/AIAS_NEXT_003_RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
    missing=[name for name in manifest["artifacts"] if not (ROOT/name).is_dir()]
    assert not missing, missing
def test_release_manifest_preserves_external_gates():
    manifest=json.loads((ROOT/"engineering/aias/release_gate/AIAS_NEXT_003_RELEASE_MANIFEST.json").read_text(encoding="utf-8"))
    assert "OCCT runtime and license" in manifest["external_gates"]
    assert "legal compliance" in manifest["claims_not_made"]
