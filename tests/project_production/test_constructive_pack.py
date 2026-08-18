import json
from pathlib import Path
from aias_constructive_standards import ConstructivePackValidator
def test_pack_schema_and_fail_closed_inventory():
 p=Path(__file__).parents[2]/'engineering/aias/standards/VE_CONSTRUCTIVE_CONCRETE_PACK/VE_CONSTRUCTIVE_CONCRETE_PACK_1.0.json'; pack=json.loads(p.read_text(encoding='utf-8')); assert not ConstructivePackValidator().validate(pack); assert len(pack['rules'])==7 and pack['fail_closed_rules']
