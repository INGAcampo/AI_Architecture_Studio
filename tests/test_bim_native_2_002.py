import json
from pathlib import Path
from aias_bim_native2.fixture_validation import validate_fixture
ROOT=Path(__file__).resolve().parents[1]
def test_ifc_semantic_fixture_validates_locally():
    fixture=json.loads((ROOT/"engineering/aias/bim/BIM_NATIVE_2_002_FIXTURE.json").read_text(encoding="utf-8"))
    result=validate_fixture(fixture)
    assert result["valid"] is True and result["entity_count"] == 2
def test_fixture_validator_rejects_unknown_relationship():
    result=validate_fixture({"schema":"IFC4","entities":[{"id":"w","ifc_class":"IfcWall","relationships":["missing"],"properties":{}}]})
    assert result["valid"] is False and "unknown_relationship_target" in result["errors"]
